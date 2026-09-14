import os
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

DB_PATH = '/tmp/lost_found.db' if os.environ.get('PORT') else 'lost_found.db'

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
            claimer TEXT,
            created_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json
    beijing_time = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO items (name, feature, location, contact, created_at) VALUES (?, ?, ?, ?, ?)",
        (data['name'], data['feature'], data['location'], data['contact'], beijing_time)
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "物品已成功入库"})

@app.route('/items', methods=['GET'])
def get_items():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM items ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    items_list = []
    for row in rows:
        items_list.append({
            "id": row[0], "name": row[1], "feature": row[2],
            "location": row[3], "contact": row[4],
            "status": row[5], "claimer": row[6], "created_at": row[7]
        })
    return jsonify({"items": items_list})

@app.route('/claim_item', methods=['POST'])
def claim_item():
    data = request.json
    required = ['id', 'student_id', 'name']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({"success": False, "message": f"缺少字段：{field}"}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    claimer_info = f"姓名:{data['name']} 学号:{data['student_id']}"
    c.execute(
        "UPDATE items SET status='已认领', claimer=? WHERE id=?",
        (claimer_info, data['id'])
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": f"认领成功，{data['name']}同学"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
