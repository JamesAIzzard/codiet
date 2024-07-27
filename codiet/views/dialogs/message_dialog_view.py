from PyQt6.QtCore import pyqtSignal

from codiet.views.dialogs.label_icon_buttons_dialog_view import LabelIconButtonsDialogView
from codiet.views.buttons import OKButton

class MessageDialogView(LabelIconButtonsDialogView):
    """A simple dialog box with an OK button."""

    okClicked = pyqtSignal()

    def __init__(self, message="OK", *args, **kwargs):
        super().__init__(
            message=message,
            icon_filename="info-icon.png",
            *args, **kwargs)
        
        # Add the button
        self.btn_ok = self.add_button(OKButton())

        # Connect the button to the signal
        self.btn_ok.clicked.connect(self.okClicked)

    @property
    def message(self) -> str:
        return self.lbl_icon_message.text
    
    @message.setter
    def message(self, message: str):
        self.lbl_icon_message.text = message