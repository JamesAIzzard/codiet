from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget

from codiet.views.dialogs.base_dialog_view import BaseDialogView
from codiet.views.labels import IconTextLabel

class IconMessageDialogView(BaseDialogView):
    """A dialog box with an icon, and a message."""
    def __init__(
            self, 
            title:str = "Title",
            message:str = "Message", 
            icon_filename:str = "app-icon.png", 
            parent:QWidget|None=None,
            *args, **kwargs
        ):
        super().__init__(
            title=title,
            parent=parent,
            *args, **kwargs
        )

        # Set the top level layout
        self.lyt_top_level = QVBoxLayout(self)
        self.setLayout(self.lyt_top_level)

        # Create a horizontal layout for the icon and message
        self.lyt_icon_message = QHBoxLayout()
        self.lyt_top_level.addLayout(self.lyt_icon_message)
        # Create the iconlabel
        self.lbl_icon_message = IconTextLabel(
            icon_filename=icon_filename,
            text=message,
            parent=self
        )
        # Add the iconlabel to the layout
        self.lyt_icon_message.addWidget(self.lbl_icon_message)

        # Stash the icon size
        self._icon_size: int = 30 # Default to 30px

    @property
    def message(self):
        return self.lbl_icon_message.text

    @message.setter
    def message(self, message: str):
        self.lbl_icon_message.text = message

    def set_message_icon(self, icon_name: str) -> None:
        """Set the icon for the dialog box."""
        self.lbl_icon_message.set_icon(icon_name)
        self.lbl_icon_message.set_icon_size(self._icon_size)

    def set_message_icon_size(self, size: int) -> None:
        """Set the size of the icon."""
        self._icon_size = size
        self.lbl_icon_message.set_icon_size(size)