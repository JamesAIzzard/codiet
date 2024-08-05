import sqlite3
from typing import Generator
from contextlib import contextmanager

from codiet.db.database import Database

class RepositoryBase:
    def __init__(self, database: Database) -> None:

        self._database = database

    @property
    def connection(self) -> sqlite3.Connection:
        """Return a connection to the database."""
        return self._database.connection

    def close_connection(self) -> None:
        """Close the connection to the database."""
        self._database.connection.close()

    @contextmanager
    def get_cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        """Return a cursor for the database connection."""
        cursor = self.connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def commit(self) -> None:
        """Commit changes to the database."""
        self.connection.commit()        