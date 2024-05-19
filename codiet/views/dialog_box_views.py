from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDialogButtonBox,
    QSizePolicy,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QIcon


class DialogBoxView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the window title
        self.setWindowTitle("Custom Dialog")
        # Set the window icon
        self.setWindowIcon(QIcon("codiet/resources/icons/app-icon.png"))

        # Set the dialog layout
        lyt_top_level = QVBoxLayout(self)

        # Add an HBox for icon and label
        self.lyt_icon_and_label = QHBoxLayout()
        lyt_top_level.addLayout(self.lyt_icon_and_label)

        # Init the label for the icon
        self.lbl_icon = QLabel(self)
        self.lyt_icon_and_label.addWidget(self.lbl_icon)

        # Add the text
        self.lbl_message = QLabel(self)
        self.lbl_message.setWordWrap(True)
        self.lbl_message.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.lyt_icon_and_label.addWidget(self.lbl_message)

        # Add the buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        lyt_top_level.addWidget(self.button_box)

    @property
    def title(self):
        return self.windowTitle()

    @title.setter
    def title(self, title: str):
        self.setWindowTitle(title)

    @property
    def message(self):
        return self.lbl_message.text()

    @message.setter
    def message(self, message: str):
        self.lbl_message.setText(message)

    def set_icon(self, icon_path: str):
        """Set the icon for the dialog box."""
        # Create the pixmap to display the icon
        pixmap = QPixmap(icon_path)
        # Set the pixmap to the label
        self.lbl_icon.setPixmap(
            pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        )

    def set_button_configuration(self, buttons):
        """Set the buttons to display on the dialog box."""
        self.button_box.setStandardButtons(buttons)


class OkDialogBoxView(DialogBoxView):
    """A simple dialog box with an OK button."""

    def __init__(
        self, message: str = "Complete", title: str = "Action Complete", parent=None
    ):
        super().__init__(parent)
        self.set_button_configuration(QDialogButtonBox.StandardButton.Ok)
        self.set_icon("codiet/resources/icons/ok-icon.png")
        self.message = message
        self.title = title


class ErrorDialogBoxView(DialogBoxView):
    """A dialog box to display an error message."""

    def __init__(
        self, message: str = "An error occurred.", title: str = "Error", parent=None
    ):
        super().__init__(parent)
        self.set_button_configuration(QDialogButtonBox.StandardButton.Ok)
        self.set_icon("codiet/resources/icons/error-icon.png")
        self.message = message
        self.title = title


class ConfirmDialogBoxView(DialogBoxView):
    """A dialog box to confirm an action."""

    def __init__(
        self, message: str = "Are you sure?", title: str = "Confirm", parent=None
    ):
        super().__init__(parent)
        self.set_button_configuration(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.set_icon("codiet/resources/icons/question-icon.png")
        self.message = message
        self.title = title


class YesNoDialogBoxView(DialogBoxView):
    """A dialog box to make a Yes/No decision."""

    def __init__(
        self, message: str = "Are you sure?", title: str = "Confirm", parent=None
    ):
        super().__init__(parent)
        self.set_button_configuration(
            QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No
        )
        self.set_icon("codiet/resources/icons/question-icon.png")
        self.message = message
        self.title = title