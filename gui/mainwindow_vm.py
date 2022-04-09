from PyQt6 import QtWidgets

from .mainwindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_manage_nutrients.triggered.connect(self.on_manage_nutrients_click)
        self.ui.btn_user_requirements.triggered.connect(self.on_user_preferences_click)

    def on_manage_nutrients_click(self):
        self.ui.wg_pages.setCurrentIndex(0)

    def on_user_preferences_click(self):
        self.ui.wg_pages.setCurrentIndex(1)