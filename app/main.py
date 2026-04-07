from fastapi import FastAPI, HTTPException
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.database import get_db_connection
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Career Center Bot API",
    description="Backend API for automating career center workflows via Telegram bot",
    version="1.0.0",
)


@app.get("/", summary="Health check")
def root():
    return {"status": "ok", "service": "Career Center Bot API"}


@app.get("/tasks", response_model=List[TaskResponse], summary="Get all tasks")
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks


@app.post("/tasks", response_model=TaskResponse, status_code=201, summary="Create task")
def create_task(task: TaskCreate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO tasks (title, description, status, assigned_to) VALUES (%s, %s, %s, %s)",
        (task.title, task.description, task.status, task.assigned_to),
    )
    conn.commit()
    task_id = cursor.lastrowid
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    new_task = cursor.fetchone()
    cursor.close()
    conn.close()
    return new_task


@app.get("/tasks/{task_id}", response_model=TaskResponse, summary="Get task by ID")
def get_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, summary="Update task")
def update_task(task_id: int, task_update: TaskUpdate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    existing = cursor.fetchone()
    if not existing:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    updates = task_update.dict(exclude_unset=True)
    if updates:
        set_clause = ", ".join(f"{k} = %s" for k in updates.keys())
        values = list(updates.values()) + [task_id]
        cursor.execute(f"UPDATE tasks SET {set_clause} WHERE id = %s", values)
        conn.commit()

    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    updated = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete task")
def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    if affected == 0:
        raise HTTPException(status_code=404, detail="Task not found")
