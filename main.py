import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import qInstallMessageHandler

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
    # Create the application UI and controller
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet("main.qss"))
    window = MainWindowView()
    main_window_ctrl = MainWindowCtrl(window)
    window.show()
    sys.exit(app.exec())
