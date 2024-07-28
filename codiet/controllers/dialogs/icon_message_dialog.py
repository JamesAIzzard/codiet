from typing import TypeVar, Generic

from PyQt6.QtWidgets import QWidget
from codiet.views.dialogs.base_dialog_view import BaseDialogView
from codiet.views.dialogs.icon_message_dialog_view import IconMessageDialogView
from codiet.controllers.dialogs.base_dialog import BaseDialog

T = TypeVar('T', bound=IconMessageDialogView)

class IconMessageDialog(BaseDialog[IconMessageDialogView], Generic[T]):
    """A dialog box with an icon, and a message.
    Extends BaseDialog to add an icon and a message.
    """

    def __init__(
            self, 
            message:str = "Message",
            icon_filename:str = "app-icon.png", 
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)

        # Set the message
        self.message = message
        self.set_message_icon(icon_filename)

        self.view: IconMessageDialogView

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

    def _create_view(self, parent: QWidget, *args, **kwargs) -> IconMessageDialogView:
        return IconMessageDialogView(parent=parent, *args, **kwargs)