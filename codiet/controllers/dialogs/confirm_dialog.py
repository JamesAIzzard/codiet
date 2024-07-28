from PyQt6.QtCore import pyqtSignal

from codiet.views.icon_button import IconButton
from codiet.controllers.dialogs.icon_message_buttons_dialog import IconMessageButtonsDialog

class ConfirmDialog(IconMessageButtonsDialog):
    """A dialog box to ask the user to confirm an action.
    Specialises IconMessageButtonsDialog to add confirm and cancel buttons.
    """

    confirmClicked = pyqtSignal()
    cancelClicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        # Create a Confirm and Cancel button
        self.btn_confirm = IconButton(icon_filename="confirm-icon.png")
        self.btn_clear = IconButton(icon_filename="clear-icon.png")

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