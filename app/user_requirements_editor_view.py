from PyQt6 import QtWidgets, uic

import app

class UserRequirementsEditorView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Declare active widgets
        self.wg_flags: QtWidgets.QGroupBox

        # Bring the ui file in
        uic.load_ui.loadUi('app/user_requirements_editor.ui', self)

        # Build the flag editor widget
        self.wg_flag_selector = app.FlagSelectorView()
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.wg_flag_selector)
        vbox.setContentsMargins(0,0,0,0)
        self.wg_flags.setLayout(vbox)