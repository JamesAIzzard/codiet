import os

from codiet.db.database import Database
from codiet.db.repository import Repository

DB_PATH = os.path.join("codiet", "tests", "codiet_test.db")

def get_repository() -> Repository:
    return Repository(get_database())

def get_database() -> Database:
    return Database(DB_PATH)