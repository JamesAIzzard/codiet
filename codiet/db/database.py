import sqlite3

class Database:
    def __init__(self, DB_PATH):
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()
            
    def execute(self, query, params=()):
        return self.connection.execute(query, params)

    def fetch_all(self, query, params=()):
        with self.connection:
            return self.connection.execute(query, params).fetchall()

    def commit(self):
        self.connection.commit()