import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'todo.db')


def connect_to_db(db_path=DB_PATH):
    con = sqlite3.connect(db_path)
    return con
