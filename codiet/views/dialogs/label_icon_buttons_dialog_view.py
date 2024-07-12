from PyQt6.QtWidgets import QHBoxLayout, QPushButton

from codiet.views.dialogs.label_icon_dialog_view import LabelIconDialog

class LabelIconButtonsDialogView(LabelIconDialog):
    """A dialog box with a label, an icon, and a button box."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add a button box
        self.lyt_button_box = QHBoxLayout()
        self.lyt_top_level.addLayout(self.lyt_button_box)

    def add_button(self, button: QPushButton) -> QPushButton:
        """Add a button to the button box."""
        self.lyt_button_box.addWidget(button)
        return button