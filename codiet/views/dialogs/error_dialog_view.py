from codiet.views.dialogs.message_dialog_view import MessageDialogView

class ErrorDialogView(MessageDialogView):
    """A dialog box to display an error message."""

    def __init__(self, title="Error", message="An error occurred.", *args, **kwargs):
        super().__init__(title=title, message=message, *args, **kwargs)
        self.set_dialog_window_icon("error-icon.png")