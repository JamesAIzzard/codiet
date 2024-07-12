from PyQt6.QtCore import pyqtSignal

from codiet.views.dialogs.label_icon_buttons_dialog_view import LabelIconButtonsDialogView
from codiet.views.buttons import OKButton

class OkDialogBoxView(LabelIconButtonsDialogView):
    """A simple dialog box with an OK button."""

    okClicked = pyqtSignal()

    def __init__(self, title="OK", message="OK", *args, **kwargs):
        super().__init__(
            title=title, 
            message=message,
            icon_filename="info-icon.png",
            *args, **kwargs)
        # Add the button
        self.btn_ok = self.add_button(OKButton())
        # Connect the button to the signal
        self.btn_ok.clicked.connect(self.okClicked)