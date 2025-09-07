from flask import Flask, jsonify, request, send_from_directory, abort
import sqlite3, os
from flask_cors import CORS

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "todos.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Ensure DB exists
if not os.path.exists(DB_PATH):
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)

@app.route("/api/todos", methods=["GET"])
def list_todos():
    conn = get_db()
    rows = conn.execute("SELECT * FROM todos ORDER BY id DESC").fetchall()
    conn.close()
    todos = [dict(r) for r in rows]
    for t in todos:
        t["done"] = bool(t["done"])
    return jsonify(todos)

@app.route("/api/todos", methods=["POST"])
def create_todo():
    data = request.get_json() or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error":"Title required"}), 400
    conn = get_db()
    cur = conn.execute("INSERT INTO todos (title, done) VALUES (?,?)", (title, 0))
    conn.commit()
    todo_id = cur.lastrowid
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    conn.close()
    todo = dict(row)
    todo["done"] = bool(todo["done"])
    return jsonify(todo), 201

@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json() or {}
    title = data.get("title")
    done = data.get("done")
    if title is None and done is None:
        return jsonify({"error":"No fields to update"}), 400
    conn = get_db()
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error":"Not found"}), 404
    new_title = title if title is not None else row["title"]
    new_done = 1 if bool(done) else 0 if done is not None else row["done"]
    conn.execute("UPDATE todos SET title=?, done=? WHERE id=?", (new_title, new_done, todo_id))
    conn.commit()
    updated = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    conn.close()
    todo = dict(updated)
    todo["done"] = bool(todo["done"])
    return jsonify(todo)

@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = get_db()
    cur = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return jsonify({"error":"Not found"}), 404
    return '', 204

# Serve frontend static files
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    root = app.static_folder
    if path and os.path.exists(os.path.join(root, path)):
        return send_from_directory(root, path)
    return send_from_directory(root, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
