import sqlite3
import os

from codiet.db._create_schema import _create_schema

class Database:
    def __init__(self, DB_PATH):
        self.db_name = DB_PATH
        self.db_exists = os.path.exists(self.db_name)
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        if not self.db_exists:
            _create_schema(self.cursor)
            
    def execute(self, query, params=()):
        with self.connection:
            return self.connection.execute(query, params)

    def fetch_all(self, query, params=()):
        with self.connection:
            return self.connection.execute(query, params).fetchall()
