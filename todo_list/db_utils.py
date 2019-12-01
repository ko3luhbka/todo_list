import logging
import sqlite3

import click

from flask import current_app, g
from flask.cli import with_appcontext


def query_db(query: str, args=(), one=False):
    with get_db() as db:
        try:
            cur = db.execute(query, args)
            rv = cur.fetchall()
            if one:
                return rv[0] if rv else None
            return rv
        except sqlite3.DatabaseError as err:
            logging.exception(err)
            return err


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.cursor().executescript(f.read().decode('utf-8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
