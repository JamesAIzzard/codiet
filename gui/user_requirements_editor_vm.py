from PyQt6 import QtWidgets

from .user_requirements_editor import Ui_user_requirements_editor
from model import configs, flags, user

class UserRequirementsEditor(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_user_requirements_editor()
        self.ui.setupUi(self)

        self.populate_global_flags()

        # Handle add/remove buttons
        self.ui.btn_adopt_flag.clicked.connect(self.on_adopt_flag_click)
        self.ui.btn_remove_flag.clicked.connect(self.on_remove_flag_click)

    def on_adopt_flag_click(self):
        """Handler for clicks on the adopt flag button."""
        flag_name = flags.get_flag_name_from_string(
            self.ui.lst_global_flags.currentItem().text()
        )
        user.user.add_global_flag(flag_name)
        self.populate_user_flags()

    def on_remove_flag_click(self):
        """Handler for clicks on the remove flag button."""
        flag_name = flags.get_flag_name_from_string(
            self.ui.lst_user_flags.currentItem().text()
        )
        user.user.global_flags.remove(flag_name)
        self.populate_user_flags()

    def populate_global_flags(self):
        """Uses the flag configs to populate the list of global flags."""
        self.ui.lst_global_flags.clear()
        for flag in configs.FLAG_CONFIGS.values():
            self.ui.lst_global_flags.addItem(flag["string"])

    def populate_user_flags(self):
        """Populates list of user flags from list on user model."""
        self.ui.lst_user_flags.clear()
        for flag in user.user.global_flags:
            self.ui.lst_user_flags.addItem(configs.FLAG_CONFIGS[flag]["string"])