import sys, logging

from PyQt6.QtWidgets import QApplication

from codiet.db import DB_PATH
from codiet.db.database import Database
from codiet.db.repository import Repository
from codiet.db.database_service import DatabaseService
from codiet.views import load_stylesheet
from codiet.views.main_window_view import MainWindowView
from codiet.controllers import MainWindow

def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Set to DEBUG for development, INFO or WARNING for production
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stderr),
            # You can add file handlers here if you want to log to a file as well
        ]
    )

if __name__ == "__main__":
    # Create the application object
    app = QApplication(sys.argv)

    # Load the stylesheet
    app.setStyleSheet(load_stylesheet("main.qss"))

    # Create the database objects
    database = Database(DB_PATH)
    repository = Repository(database)
    db_service = DatabaseService(repository)

    # Create the main window
    main_window = MainWindow(
        view=MainWindowView(),
        db_service=db_service
    )
    # Show the main window
    main_window.show()
    # Run the application
    sys.exit(app.exec())
