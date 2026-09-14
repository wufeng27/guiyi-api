import os
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
DB_PATH = 'lost_found.db'

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            feature TEXT,
            location TEXT,
            contact TEXT,
            status TEXT DEFAULT '待认领',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/add_item', methods=['POST'])
def add_item():
    """拾主上交，写入数据库"""
   data = request.get_json(force=True, silent=True) or request.json
    required = ['name', 'feature', 'location', 'contact']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({"success": False, "message": f"缺少字段：{field}"}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO items (name, feature, location, contact) VALUES (?, ?, ?, ?)",
        (data['name'], data['feature'], data['location'], data['contact'])
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "物品已成功入库，等待失主认领"})

@app.route('/items', methods=['GET'])
def get_items():
    """查询所有物品（调试用）"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM items ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return jsonify({"items": rows})

if __name__ == '__main__':
    init_db()
    # 云端会自动分配 PORT 环境变量
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
