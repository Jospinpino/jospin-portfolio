"""TaskFlow API, a small Flask REST API for managing tasks.

Backend counterpart to the TaskFlow web app in the portfolio. Stores tasks in
a local SQLite database and exposes a JSON CRUD API.
"""

import sqlite3
from pathlib import Path

from flask import Flask, g, jsonify, request

DB_PATH = Path(__file__).parent / "taskflow.db"
VALID_STATUSES = {"todo", "doing", "done"}
VALID_PRIORITIES = {"low", "medium", "high"}


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'medium',
                status TEXT NOT NULL DEFAULT 'todo',
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def create_app(db_path=None):
    app = Flask(__name__)

    global DB_PATH
    if db_path:
        DB_PATH = Path(db_path)

    init_db()

    @app.teardown_appcontext
    def close_db(exception=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def task_to_dict(row):
        return {
            "id": row["id"],
            "title": row["title"],
            "priority": row["priority"],
            "status": row["status"],
            "created_at": row["created_at"],
        }

    @app.get("/api/tasks")
    def list_tasks():
        status = request.args.get("status")
        db = get_db()
        if status:
            if status not in VALID_STATUSES:
                return jsonify({"error": f"invalid status filter: {status}"}), 400
            rows = db.execute(
                "SELECT * FROM tasks WHERE status = ? ORDER BY id DESC", (status,)
            ).fetchall()
        else:
            rows = db.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
        return jsonify([task_to_dict(r) for r in rows])

    @app.get("/api/tasks/stats")
    def task_stats():
        db = get_db()
        rows = db.execute(
            "SELECT status, COUNT(*) as count FROM tasks GROUP BY status"
        ).fetchall()
        stats = {status: 0 for status in VALID_STATUSES}
        for row in rows:
            stats[row["status"]] = row["count"]
        stats["total"] = sum(stats.values())
        return jsonify(stats)

    @app.get("/api/tasks/<int:task_id>")
    def get_task(task_id):
        db = get_db()
        row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            return jsonify({"error": "task not found"}), 404
        return jsonify(task_to_dict(row))

    @app.post("/api/tasks")
    def create_task():
        data = request.get_json(silent=True) or {}
        title = (data.get("title") or "").strip()
        priority = data.get("priority", "medium")
        status = data.get("status", "todo")

        if not title:
            return jsonify({"error": "title is required"}), 400
        if priority not in VALID_PRIORITIES:
            return jsonify({"error": f"invalid priority: {priority}"}), 400
        if status not in VALID_STATUSES:
            return jsonify({"error": f"invalid status: {status}"}), 400

        db = get_db()
        cur = db.execute(
            "INSERT INTO tasks (title, priority, status) VALUES (?, ?, ?)",
            (title, priority, status),
        )
        db.commit()
        row = db.execute("SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)).fetchone()
        return jsonify(task_to_dict(row)), 201

    @app.patch("/api/tasks/<int:task_id>")
    def update_task(task_id):
        db = get_db()
        row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            return jsonify({"error": "task not found"}), 404

        data = request.get_json(silent=True) or {}
        title = data.get("title", row["title"])
        priority = data.get("priority", row["priority"])
        status = data.get("status", row["status"])

        if priority not in VALID_PRIORITIES:
            return jsonify({"error": f"invalid priority: {priority}"}), 400
        if status not in VALID_STATUSES:
            return jsonify({"error": f"invalid status: {status}"}), 400

        db.execute(
            "UPDATE tasks SET title = ?, priority = ?, status = ? WHERE id = ?",
            (title, priority, status, task_id),
        )
        db.commit()
        row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return jsonify(task_to_dict(row))

    @app.delete("/api/tasks/<int:task_id>")
    def delete_task(task_id):
        db = get_db()
        row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            return jsonify({"error": "task not found"}), 404
        db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        db.commit()
        return "", 204

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
