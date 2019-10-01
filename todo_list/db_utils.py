import os
import logging
import sqlite3

from todo_list.todo_task import TaskStatus

DB_PATH = os.path.join(os.path.dirname(__file__), "todo.db")


def connect_to_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    return conn


def add_task(task):
    """Add new todo list task"""

    logging.info("adding task [%s]", task)
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks(task, status) VALUES(?,?)",
            (task, TaskStatus.not_started.value),
        )
        conn.commit()
        return {"task": task, "status": TaskStatus.not_started.value}

    except Exception as err:
        logging.error("Error : %s", err)
        return None


def get_all_tasks():
    """Get all todo list tasks"""

    logging.info("getting all tasks")
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("select * from tasks")
        rows = cur.fetchall()
        return {"count: ": len(rows), "tasks": rows}

    except Exception as err:
        logging.error("Error : %s", err)
        return None


def get_task(task):
    """Get one todo list task by name"""

    logging.info("getting task [%s]", task)
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(f"select status from tasks where task='{task}'")
        status = cur.fetchone()[0]
        return status
    except Exception as err:
        logging.error("Error : %s", err)
        return None


def update_status(task, status):
    """Update todo list task status"""

    logging.info(
        "updating status of task [%s] to [%s]",
        task,
        status,
    )
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("update tasks set status=? where task=?", (status, task))
        conn.commit()
        return {task: status}
    
    except Exception as err:
        logging.error("Error: %s", err)
        return None


def delete_task(task):
    """Delete task by name"""

    logging.info("deleting task [%s]", task)
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("delete from tasks where task=?", (task,))
        conn.commit()
        return {"task": task}
    except Exception as err:
        logging.error("Error: %s", err)
        return None
