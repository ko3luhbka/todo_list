import logging
import os
import sqlite3

from flask import current_app

from typing import Optional, Union

from todo_list.todo_task import TaskStatus


class QueryDB:
    """Class contains SQLite database query methods."""

    def __init__(self):
        self.db_path = current_app.config['DATABASE']
        try:
            self.db_connection = self._connect_to_db()
            self.db_cursor = self.db_connection.cursor()
        except sqlite3.DatabaseError:
            logging.exception("Database connection error")

    def add_task(self, task: str) -> Union[dict, str]:
        """Add new todo list task."""
        logging.info("Adding task [%s]", task)
        try:
            self.db_cursor.execute(
                "INSERT INTO tasks(task, status) VALUES(?,?)",
                (task, TaskStatus.not_started.value),
            )
            self.db_connection.commit()
            return {"task": task, "status": TaskStatus.not_started.value}
        except sqlite3.IntegrityError:
            err_msg = "Error: task '{0}' already exists!".format(task)
            logging.exception(err_msg)
            return err_msg

    def get_all_tasks(self) -> Optional[dict]:
        """Get all todo list tasks."""
        logging.info("Getting all tasks")
        try:
            self.db_cursor.execute("SELECT * FROM tasks")
            rows = self.db_cursor.fetchall()
            return {"count: ": len(rows), "tasks": rows}
        except sqlite3.DatabaseError:
            logging.exception("Error while getting all tasks")
            return None

    def get_task(self, task: str) -> Optional[dict]:
        """Get one todo list task by name."""
        logging.info("Getting task [%s]", task)
        try:
            self.db_cursor.execute(
                f"SELECT status FROM tasks WHERE task='{task}'"
            )
            return self.db_cursor.fetchone()[0]
        except sqlite3.DatabaseError:
            logging.exception("Error while getting task {0}", task)
            return None

    def update_status(self, task: str, status: str) -> Optional[dict]:
        """Update todo list task status."""
        logging.info("Updating status of task [%s] to [%s]", task, status)
        try:
            self.db_cursor.execute(
                "UPDATE tasks SET status=? WHERE task=?",
                (status, task),
            )
            self.db_connection.commit()
            return {task: status}
        except sqlite3.DatabaseError:
            logging.exception("Error while updating status of task '{0}'", task)
            return None

    def delete_task(self, task: str) -> Optional[dict]:
        """Delete task by name."""
        logging.info("Deleting task [%s]", task)
        try:
            self.db_cursor.execute("DELETE FROM tasks WHERE task=?", (task,))
            self.db_connection.commit()
            return {"task": task}
        except sqlite3.DatabaseError:
            logging.exception("Error while deleting task '{0}'", task)
            return None

    def _connect_to_db(self):
        # It's safe to set `check_same_thread` argument to False because
        # we work in single thread
        return sqlite3.connect(self.db_path, check_same_thread=False)
