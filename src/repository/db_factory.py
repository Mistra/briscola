import sqlite3

from flask import current_app, g


def get_db_connection():
    if 'db' not in g:
        # ignore_warnings(pylint)
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    database_conn = g.pop('db', None)

    if database_conn is not None:
        database_conn.close()
