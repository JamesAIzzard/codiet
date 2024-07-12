from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

from codiet.views.dialogs.dialog_view import DialogView
from codiet.views.labels import IconTextLabel

class LabelIconDialog(DialogView):
    """A dialog box with a label and an icon."""
    def __init__(
            self, 
            message:str = "Message", 
            icon_filename:str = "app-icon.png", 
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)

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

    @property
    def message(self):
        return self.lbl_icon_message.text

    @message.setter
    def message(self, message: str):
        self.lbl_icon_message.text = message

    def set_icon(self, icon_name: str):
        """Set the icon for the dialog box."""
        self.lbl_icon_message.set_icon(icon_name)
        self.lbl_icon_message.set_icon_size(30)