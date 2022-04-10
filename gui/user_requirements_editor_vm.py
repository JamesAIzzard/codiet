from PyQt6 import QtWidgets

from .user_requirements_editor import Ui_user_requirements_editor
from model import FLAG_CONFIGS

class UserRequirementsEditor(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_user_requirements_editor()
        self.ui.setupUi(self)

        self.populate_global_flags()

    def populate_global_flags(self):
        """Uses the flag configs to populate the list of global flags."""
        for flag in FLAG_CONFIGS.values():
            self.ui.lst_global_flags.addItem(flag["string"])