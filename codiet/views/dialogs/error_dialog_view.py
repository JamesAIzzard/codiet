from codiet.views.dialogs.ok_button_dialog_view import OkDialogBoxView

class ErrorDialogBoxView(OkDialogBoxView):
    """A dialog box to display an error message."""

    def __init__(self, title="Error", message="An error occurred.", *args, **kwargs):
        super().__init__(title=title, message=message, *args, **kwargs)
        self.set_icon("error-icon.png")