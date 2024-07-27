from PyQt6.QtCore import pyqtSignal

from codiet.views.buttons import ConfirmButton
from codiet.controllers.dialogs.icon_message_buttons_dialog import IconMessageButtonsDialog

class ErrorDialog(IconMessageButtonsDialog):
    """A specific type of message dialog for displaying errors.
    Specialises the IconMessageButtonsDialog to show the error Icon and an OK button.
    """

    okClicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        # Create the OK button
        self.btn_OK = ConfirmButton()

        super().__init__(
            icon_filename="error-icon.png",
            buttons=[
                self.btn_OK
            ],
            *args, **kwargs
        )

        # Connect the OK button to its signal
        self.btn_OK.clicked.connect(self.okClicked)