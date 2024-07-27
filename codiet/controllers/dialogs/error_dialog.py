from PyQt6.QtWidgets import QWidget

from codiet.views.dialogs.error_dialog_view import ErrorDialogView
from codiet.controllers.dialogs.message_dialog import MessageDialog

class ErrorDialog(MessageDialog):
    """A specific type of message dialog for dipslaying errors."""
    def __init__(
            self, 
            view: ErrorDialogView|None=None,
            parent: QWidget|None=None, 
            title:str|None=None, 
            message:str|None=None,
            *args, **kwargs
        ):
        super().__init__(
            view=view,
            parent=parent,
            view_type=ErrorDialogView,
            title=title,
            message=message,
            message_icon="error.png",
            *args, **kwargs
        )