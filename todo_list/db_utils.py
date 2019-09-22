import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'todo.db')
# ToDo list items statuses
NOTSTARTED = 'Not Started'
INPROGRESS = 'In Progress'
COMPLETED = 'Completed'


def connect_to_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    return conn


def add_item(item):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO items(item, status) VALUES(?,?)',
            (item, NOTSTARTED)
        )
        conn.commit()
        return {'item': item, 'status': NOTSTARTED}
    except Exception as e:
        print('Error: ', e)
        return None


def get_all_items():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('select * from items')
        rows = cur.fetchall()
        return {'count: ': len(rows), 'items': rows}
    except Exception as e:
        print('Error: ', e)
        return None


def get_item(item):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(f"select status from items where item='{item}'")
        status = cur.fetchone()[0]
        return status
    except Exception as e:
        print('Error: ', e)
        return None


def update_status(item, status):
    status_lower = status.lower().strip()
    if status_lower == 'not started':
        status = NOTSTARTED
    elif status_lower == 'in progress':
        status = INPROGRESS
    elif status_lower == 'completed':
        status = COMPLETED
    else:
        print("Invalid status: ", status)
        return None

    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('update items set status=? where item=?', (status, item))
        conn.commit()
        return {item: status}
    except Exception as e:
        print('Error: ', e)
        return None


def delete_item(item):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('delete from items where item=?', (item,))
        conn.commit()
        return {'item': item}
    except Exception as e:
        print('Error: ', e)
        return None
