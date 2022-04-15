from PyQt6 import QtWidgets

from .mainwindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect the menu buttons to the page change handlers
        self.ui.btn_manage_nutrients.triggered.connect(
            lambda: self.change_window(0)
        )
        self.ui.btn_user_requirements.triggered.connect(
            lambda: self.change_window(1)
        )

    def change_window(self, page_id: int):
        """Updates the main window to show the pane with the
        specified ID."""
        self.ui.wg_pages.setCurrentIndex(page_id)