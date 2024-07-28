from codiet.views.icon_button import IconButton
from codiet.controllers.dialogs.icon_message_buttons_dialog import IconMessageButtonsDialog

class YesNoDialog(IconMessageButtonsDialog):
    """A dialog box to ask the user to confirm an action.
    Specialises IconMessageButtonsDialog to add confirm and cancel buttons.
    """

    def __init__(self, *args, **kwargs):
        # Create a Confirm and Cancel button
        self.btn_yes = IconButton(icon_filename="ok-icon.png")
        self.btn_no = IconButton(icon_filename="cancel-icon.png")

        super().__init__(
            icon_filename="question-icon.png",
            buttons=[
                self.btn_yes,
                self.btn_no
            ],
            *args, **kwargs
        )