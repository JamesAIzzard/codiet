import os
import tempfile
import unittest

from codiet.db.database import Database
from codiet.db.repository import Repository
from codiet.db.database_service import DatabaseService

class DatabaseTestCase(unittest.TestCase):
    """Base class for Repository test cases."""

    def setUp(self):
        """Set up the test case."""
        # Create a temporary file for the database
        self.temp_db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db_file.name
        # Init the database classes
        self.database = Database(self.db_path)
        self.repository = Repository(self.database)
        self.database_service = DatabaseService(self.repository)
        # Create the database
        self.database._create_database()

    def tearDown(self) -> None:
        """Tear down the test case."""
        self.repository.close_connection()
        self.temp_db_file.close()
        os.unlink(self.db_path)