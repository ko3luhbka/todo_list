import os
import sqlite3

from todo_list.todo_task import TaskStatus

DB_PATH = os.path.join(os.path.dirname(__file__), 'todo.db')


def connect_to_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    return conn


def add_item(item):
    print(f'=== adding item [{item}]')
    try:
        print('=== item: ', item)
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO items(item, status) VALUES(?,?)',
            (item, TaskStatus.NOTSTARTED.value)
        )
        conn.commit()
        return {'item': item, 'status': TaskStatus.NOTSTARTED.value}

    except Exception as e:
        print('Error: ', e)
        return None


def get_all_items():
    print('=== getting all items')
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('select * from items')
        rows = cur.fetchall()
        return {'count: ': len(rows), 'items': rows}

    except Exception as e:
        print('=== Error: ', e)
        return None


def get_item(item):
    print(f'=== getting item [{item}]')
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(f"select status from items where item='{item}'")
        status = cur.fetchone()[0]
        return status
    except Exception as e:
        print('=== Error: ', e)
        return None


def update_status(item, status):
    print(f'=== updating status of item [{item}] to [{status}]')
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
    print(f'=== deleting item [{item}]')
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('delete from items where item=?', (item,))
        conn.commit()
        return {'item': item}
    except Exception as e:
        print('=== Error: ', e)
        return None
