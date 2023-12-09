import sys, os

from PyQt6.QtWidgets import QApplication

from codiet.views.main_window_view import MainWindowView
from codiet.controllers.main_window_ctrl import MainWindowCtrl
from codiet.db.database import Database
from codiet.db.repository import Repository
from codiet.db.database_service import DatabaseService
from codiet.db._populate_database import _populate_ingredients, _populate_flags

DB_PATH = os.path.join("codiet", "db", "codiet.db")

if __name__ == "__main__":
    # Check if the database file exists
    if not os.path.exists(DB_PATH):
        # Create a new database and populate it with data
        db = Database(DB_PATH)
        repo = Repository(db)
        db_service = DatabaseService(repo)
        _populate_flags(db_service)
        _populate_ingredients(db_service)
    else:
        # Open the existing database
        db = Database(DB_PATH)
        repo = Repository(db)
        db_service = DatabaseService(repo)

    # Create the application UI and controller
    app = QApplication(sys.argv)
    window = MainWindowView()
    main_window_ctrl = MainWindowCtrl(window, db_service)
    window.show()
    sys.exit(app.exec())