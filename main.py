import sys, os

from PyQt6.QtWidgets import QApplication

from codiet.views.main_window_view import MainWindowView
from codiet.controllers.main_window_ctrl import MainWindowCtrl
from codiet.db.database import Database
from codiet.db.repository import Repository
from codiet.db.database_service import DatabaseService
from codiet.db._populate_database import (
    push_ingredients_to_db,
    push_flags_to_db,
    push_nutrients_to_db,
    remove_redundant_flags_from_datafiles,
    init_ingredient_datafiles,
    populate_ingredient_datafiles
)

DB_PATH = os.path.join("codiet", "db", "codiet.db")
RESET_DB = True

if __name__ == "__main__":
    # Check if the database file exists
    if RESET_DB:
        print("Resetting database...")
        # Delete the existing database if exists
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        # Create a new database and populate it with data
        db = Database(DB_PATH)
        repo = Repository(db)
        db_service = DatabaseService(repo)
        push_flags_to_db(db_service)
        push_nutrients_to_db(db_service)
        remove_redundant_flags_from_datafiles(db_service)
        init_ingredient_datafiles(db_service)
        populate_ingredient_datafiles(db_service)
        push_ingredients_to_db(db_service)
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
