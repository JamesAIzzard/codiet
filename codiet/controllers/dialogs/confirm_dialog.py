from PyQt6.QtCore import pyqtSignal

from codiet.views.buttons import ConfirmButton, ClearButton
from codiet.controllers.dialogs.icon_message_buttons_dialog import IconMessageButtonsDialog

class ConfirmDialog(IconMessageButtonsDialog):
    """A dialog box to ask the user to confirm an action.
    Specialises IconMessageButtonsDialog to add confirm and cancel buttons.
    """

    confirmClicked = pyqtSignal()
    cancelClicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        # Create a Confirm and Cancel button
        self.btn_confirm = ConfirmButton()
        self.btn_clear = ClearButton()

        super().__init__(
            icon_filename="question-icon.png",
            buttons=[
                self.btn_confirm,
                self.btn_clear
            ],
            *args, **kwargs
        )

        # Connect the buttons to their signals
        self.btn_confirm.clicked.connect(self.confirmClicked)
        self.btn_clear.clicked.connect(self.cancelClicked) 