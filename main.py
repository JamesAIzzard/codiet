import sys

from PyQt6.QtWidgets import QApplication

from codiet.views.utils import load_stylesheet
from codiet.views.main_window_view import MainWindowView
from codiet.controllers.main_window_ctrl import MainWindowCtrl
from codiet.db import DB_PATH
from codiet.db.database import Database
from codiet.db.repository import Repository
from codiet.db.database_service import DatabaseService


if __name__ == "__main__":
    # Create the application UI and controller
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet("main.qss"))
    window = MainWindowView()
    main_window_ctrl = MainWindowCtrl(window)
    window.show()
    sys.exit(app.exec())
