import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import qInstallMessageHandler

from codiet.db import DB_PATH
from codiet.db.database import Database
from codiet.db.repository import Repository
from codiet.db.database_service import DatabaseService
from codiet.views import load_stylesheet
from codiet.views.main_window_view import MainWindowView
from codiet.controllers.main_window_ctrl import MainWindowCtrl


def pyqt_message_breakpoint(*args, **kwargs):
    # Print the message
    print(args, kwargs)
    breakpoint()

if __name__ == "__main__":
    # Install the custom message handler
    qInstallMessageHandler(pyqt_message_breakpoint) # type: ignore
    # Create the application object
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet("main.qss"))
    # Create the database objects
    database = Database(DB_PATH)
    repository = Repository(database)
    db_service = DatabaseService(repository)
    # Create the main window
    window = MainWindowView()
    main_window_ctrl = MainWindowCtrl(
        view=window,
        db_service=db_service
    )
    window.show()
    sys.exit(app.exec())
