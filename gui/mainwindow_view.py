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

    def change_window(self, page_id: int):
        """Updates the main window to show the pane with the
        specified ID."""
        print(f'change to {page_id}')
        self.wg_page_stack.setCurrentIndex(page_id)
