from PyQt6.QtWidgets import QWidget

from codiet.views.dialogs.message_dialog_view import MessageDialogView
from codiet.controllers.dialogs.base_dialog import BaseDialog

class MessageDialog(BaseDialog):
    def __init__(
            self,
            title:str|None=None,
            message:str|None=None,
            view: MessageDialogView|None=None,
            parent: QWidget|None=None,
            message_icon: str = "info-icon.png",
            *args, **kwargs
        ):
        super().__init__(
            title=title,
            message=message,
            parent=parent,
            view=view,
            view_type=MessageDialogView,
            *args, **kwargs
        )

        # Tell the linting tool that self.view is an OKDialogView
        self.view: MessageDialogView
        
        # Set the icon for the dialog box.
        self.view.set_label_icon(message_icon)
    
    @property
    def message(self) -> str:
        """Get the message of the dialog box."""
        return self.view.message
    
    @message.setter
    def message(self, message: str):
        """Set the message of the dialog box."""
        self.view.message = message
