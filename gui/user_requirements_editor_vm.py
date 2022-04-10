from PyQt6 import QtWidgets

from .user_requirements_editor import Ui_user_requirements_editor


class UserRequirementsEditor(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_user_requirements_editor()
        self.ui.setupUi(self)