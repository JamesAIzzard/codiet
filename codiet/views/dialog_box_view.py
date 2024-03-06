from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QDialogButtonBox,
    QSizePolicy,
)
from PyQt6.QtGui import QPixmap


class DialogBoxView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the window title
        self.setWindowTitle("Custom Dialog")

        # Set the dialog layout
        layout = QVBoxLayout(self)

        # Init the label for the icon
        self.lbl_icon = QLabel(self)
        self.lbl_icon.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.lbl_icon)

        # Add the text
        self.lbl_message = QLabel(self)
        self.lbl_message.setWordWrap(True)
        self.lbl_message.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.lbl_message)

        # Add the buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def set_icon(self, icon_path: str):
        """Set the icon for the dialog box."""
        # Create the pixmap to display the icon
        pixmap = QPixmap(icon_path)
        # Set the pixmap to the label
        self.lbl_icon.setPixmap(pixmap.scaled(64, 64, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))

    def set_text(self, text: str):
        """Set the text for the dialog box."""
        self.lbl_message.setText(text)

    def set_button_configuration(self, buttons):
        """Set the buttons to display on the dialog box."""
        self.button_box.setStandardButtons(buttons)

class OkDialogBoxView(DialogBoxView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_button_configuration(QDialogButtonBox.StandardButton.Ok)
        self.set_icon("resources/icons/ok.png")