import os
import random
import sqlite3
from flask import Flask, request, send_file

app = Flask(__name__)
IMAGE_FOLDER = "."
DATABASE = "/tmp/code_image.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS code_image (
            code TEXT PRIMARY KEY,
            image_name TEXT
        )
    """)
    conn.close()

@app.route('/view')
def view():
    code = request.args.get('code')
    if not code:
        return "❌ 无效二维码", 400

    init_db()
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT image_name FROM code_image WHERE code = ?", (code,))
    row = cur.fetchone()

    if row:
        image_name = row[0]
    else:
        all_files = os.listdir(IMAGE_FOLDER)
        images = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg')) and os.path.isfile(f)]
        if not images:
            return "⚠️ 无图片", 500
        image_name = random.choice(images)
        cur.execute("INSERT OR IGNORE INTO code_image (code, image_name) VALUES (?, ?)", (code, image_name))
        conn.commit()

    conn.close()
    return send_file(image_name)

@app.route('/')
def home():
    return "✅ 服务运行中"

if __name__ == '__main__':
    app.run()
