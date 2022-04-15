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
        page = self.wg_page_stack.findChild(QtWidgets.QWidget, page_name)
        self.wg_page_stack.setCurrentWidget(page) # type: ignore
        # self.wg_page_stack.setCurrentIndex(page_id)
