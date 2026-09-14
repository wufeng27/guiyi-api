import os
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

DB_PATH = '/tmp/lost_found.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, feature TEXT, location TEXT, contact TEXT, status TEXT DEFAULT "待认领", created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

init_db()

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO items (name, feature, location, contact) VALUES (?, ?, ?, ?)', (data['name'], data['feature'], data['location'], data['contact']))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "物品已成功入库"})

@app.route('/items', methods=['GET'])
def get_items():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM items ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return jsonify({"items": rows})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
