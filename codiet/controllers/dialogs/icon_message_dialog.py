from codiet.views.dialogs.icon_message_dialog_view import IconMessageDialogView
from codiet.controllers.dialogs.base_dialog import BaseDialog

class IconMessageDialog(BaseDialog):
    """A dialog box with an icon, and a message."""

    def __init__(
            self, 
            message:str = "Message",
            icon_filename:str = "app-icon.png", 
            *args, **kwargs
        ):
        super().__init__(
            view_type=IconMessageDialogView,
            *args, **kwargs
        )

        # Set the message
        self.message = message
        self.set_message_icon(icon_filename)


    @property
    def message(self) -> str:
        """Get the message in the dialog box."""
        return self.view.message
    
    @message.setter
    def message(self, message: str):
        self.view.message = message

    def set_message_icon(self, icon_name: str) -> None:
        """Set the icon for the dialog box."""
        self.view.set_message_icon(icon_name)

    def set_message_icon_size(self, size: int) -> None:
        """Set the size of the icon."""
        self.view.set_message_icon_size(size)