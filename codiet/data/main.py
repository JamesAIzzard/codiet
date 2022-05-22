import typing

import sqlite3

_conn:typing.Optional[sqlite3.Connection] = None
_cursor:typing.Optional[sqlite3.Cursor] = None

def connect() -> typing.Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """Returns the connection and cursor object for the database.
    Both of these are cached, so only instantiated on first use.
    """
    global _conn, _cursor
    if _conn is None:
        _conn = sqlite3.connect("codiet/data/codiet.db")
    if _cursor is None:
        _cursor = _conn.cursor()
    return _conn, _cursor



