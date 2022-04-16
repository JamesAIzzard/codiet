from PyQt6 import QtWidgets, uic, QtGui

import gui

class MainWindowView(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Declare the active widgets
        self.btn_user_requirements: QtGui.QAction
        self.btn_add_ingredient: QtGui.QAction
        self.wg_page_stack: QtWidgets.QStackedWidget

        # Bring the ui file in
        uic.load_ui.loadUi("gui/mainwindow.ui", self)

    def change_window(self, page_name: str):
        """Updates the main window to show the pane with the
        specified ID."""
        # Find the child widget by the name requested
        page = self.wg_page_stack.findChild(QtWidgets.QWidget, page_name)
        # Set the widget as current
        self.wg_page_stack.setCurrentWidget(page) # type: ignore
