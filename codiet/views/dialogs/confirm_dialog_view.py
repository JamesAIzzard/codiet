from PyQt6.QtCore import pyqtSignal

from codiet.views.dialogs.label_icon_buttons_dialog_view import LabelIconButtonsDialogView
from codiet.views.buttons import ConfirmButton, ClearButton

class ConfirmDialogBoxView(LabelIconButtonsDialogView):
    """A dialog box to confirm an action."""

    confirmClicked = pyqtSignal()
    cancelClicked = pyqtSignal()

    def __init__(self, title="Confirm", message="Are you sure?", *args, **kwargs):
        super().__init__(title=title, message=message, icon_filename="question-icon.png", *args, **kwargs)
        self.btn_confirm = self.add_button(ConfirmButton())
        self.btn_clear = self.add_button(ClearButton())
        self.btn_confirm.clicked.connect(self.confirmClicked)
        self.btn_clear.clicked.connect(self.cancelClicked)