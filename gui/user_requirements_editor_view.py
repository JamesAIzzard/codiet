from PyQt6 import QtWidgets, uic

class UserRequirementsEditorView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Declare active widgets
        self.btn_adopt_flag: QtWidgets.QPushButton
        self.btn_remove_flag: QtWidgets.QPushButton
        self.lst_user_flags: QtWidgets.QListWidget
        self.lst_global_flags: QtWidgets.QListWidget

        # Bring the ui file in
        uic.load_ui.loadUi('gui/user_requirements_editor.ui', self)