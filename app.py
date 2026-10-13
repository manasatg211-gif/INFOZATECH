from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "tasks.db"

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-before-deployment"


def get_db_connection():
    """Open a SQLite connection and return rows by column name."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the tasks table if it does not already exist."""
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                priority TEXT NOT NULL DEFAULT 'Medium'
                    CHECK(priority IN ('Low', 'Medium', 'High')),
                due_date TEXT,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


@app.route("/", methods=["GET"])
def index():
    search = request.args.get("q", "").strip()
    status = request.args.get("status", "all")
    priority = request.args.get("priority", "all")

    conditions = []
    parameters = []

    if search:
        conditions.append("(title LIKE ? OR description LIKE ?)")
        wildcard = f"%{search}%"
        parameters.extend([wildcard, wildcard])

    if status == "pending":
        conditions.append("completed = 0")
    elif status == "completed":
        conditions.append("completed = 1")
    else:
        status = "all"

    if priority in ("Low", "Medium", "High"):
        conditions.append("priority = ?")
        parameters.append(priority)
    else:
        priority = "all"

    sql = "SELECT * FROM tasks"
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += """
        ORDER BY completed ASC,
        CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END,
        CASE WHEN due_date IS NULL OR due_date = '' THEN 1 ELSE 0 END,
        due_date ASC,
        id DESC
    """

    with get_db_connection() as connection:
        tasks = connection.execute(sql, parameters).fetchall()
        totals = connection.execute(
            """
            SELECT COUNT(*) AS total,
                   SUM(CASE WHEN completed = 0 THEN 1 ELSE 0 END) AS pending,
                   SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) AS completed
            FROM tasks
            """
        ).fetchone()

    return render_template(
        "index.html",
        tasks=tasks,
        search=search,
        status=status,
        priority=priority,
        today=date.today().isoformat(),
        total=totals["total"] or 0,
        pending=totals["pending"] or 0,
        completed=totals["completed"] or 0,
    )


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "Medium")
    due_date = request.form.get("due_date", "").strip() or None

    if not title:
        flash("Please enter a task title.", "error")
        return redirect(url_for("index"))

    if len(title) > 120:
        flash("Task title must be 120 characters or fewer.", "error")
        return redirect(url_for("index"))

    if len(description) > 1000:
        flash("Description must be 1,000 characters or fewer.", "error")
        return redirect(url_for("index"))

    if priority not in ("Low", "Medium", "High"):
        priority = "Medium"

    if due_date:
        try:
            date.fromisoformat(due_date)
        except ValueError:
            flash("Please enter a valid due date.", "error")
            return redirect(url_for("index"))

    with get_db_connection() as connection:
        connection.execute(
            "INSERT INTO tasks (title, description, priority, due_date) VALUES (?, ?, ?, ?)",
            (title, description, priority, due_date),
        )

    flash("Task added successfully.", "success")
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    with get_db_connection() as connection:
        task = connection.execute(
            "SELECT completed FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

        if task is None:
            flash("Task not found.", "error")
        else:
            new_status = 0 if task["completed"] else 1
            connection.execute(
                "UPDATE tasks SET completed = ? WHERE id = ?",
                (new_status, task_id),
            )
            flash(
                "Task marked as complete." if new_status else "Task marked as pending.",
                "success",
            )

    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    with get_db_connection() as connection:
        cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount:
            flash("Task deleted.", "success")
        else:
            flash("Task not found.", "error")
    return redirect(url_for("index"))


@app.route("/clear-completed", methods=["POST"])
def clear_completed():
    with get_db_connection() as connection:
        cursor = connection.execute("DELETE FROM tasks WHERE completed = 1")
    flash(f"Removed {cursor.rowcount} completed task(s).", "success")
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
