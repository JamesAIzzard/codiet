from codiet.views.icon_button import IconButton
from codiet.controllers.dialogs.icon_message_buttons_dialog import IconMessageButtonsDialog

class OKDialog(IconMessageButtonsDialog):
    """A specific type of message dialog for displaying errors.
    Specialises the IconMessageButtonsDialog to show the error Icon and an OK button.
    """


    def __init__(self, *args, **kwargs):
        # Create the OK button
        self.btn_OK = IconButton(icon_filename="ok-icon.png", text="OK")

        super().__init__(
            icon_filename="ok-icon.png",
            buttons=[
                self.btn_OK
            ],
            *args, **kwargs
        )