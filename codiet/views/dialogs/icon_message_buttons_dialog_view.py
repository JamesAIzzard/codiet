from PyQt6.QtWidgets import QHBoxLayout, QPushButton

from codiet.views.dialogs.icon_message_dialog_view import IconMessageDialogView

class IconMessageButtonsDialogView(IconMessageDialogView):
    """A dialog box with a label, an icon, and a button box.
    Extends the icon message dialog view to include a button box.
    """

    def __init__(
            self, 
            buttons: list[QPushButton]|None = None,
            *args, **kwargs,
        ):
        super().__init__(*args, **kwargs)
        
        # Add a button box
        self.lyt_button_box = QHBoxLayout()
        self.lyt_top_level.addLayout(self.lyt_button_box)

        # If buttons are provided, add them
        if buttons is not None:
            for button in buttons:
                self.add_button(button)

    def add_button(self, button:QPushButton) -> QPushButton:
        """Add a button to the button box."""
        self.lyt_button_box.addWidget(button)
        return button