import os
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
# 解决中文乱码问题
app.config['JSON_AS_ASCII'] = False

DB_PATH = '/tmp/lost_found.db'

def init_db():
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

# 启动时初始化数据库
init_db()

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json
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
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM items ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    # 直接返回列表，不要再包一层 items，方便前端调试
    return jsonify({"items": rows})

if __name__ == '__main__':
    # 云端会自动分配 PORT 环境变量
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
