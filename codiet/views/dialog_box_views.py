from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox,
    QSizePolicy,
    QStackedWidget
)

from codiet.views import load_icon, load_pixmap_icon
from codiet.views.buttons import ConfirmButton, ClearButton
from codiet.views.labels import IconLabel

class DialogBoxView(QDialog):
    """A base class for dialog boxes with the codiet logo."""
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the window title
        self.setWindowTitle("Custom Dialog")
        # Set the window icon
        self.setWindowIcon(load_icon("app-icon.png"))

    @property
    def title(self):
        return self.windowTitle()

    @title.setter
    def title(self, title: str):
        self.setWindowTitle(title)

class LabelIconDialog(DialogBoxView):
    """A dialog box with a label and an icon."""
    def __init__(self, parent=None):
        super().__init__(parent)

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
    def message(self):
        return self.lbl_message.text()

    @message.setter
    def message(self, message: str):
        self.lbl_message.setText(message)

    def set_icon(self, icon_name: str):
        """Set the icon for the dialog box."""
        # Create the pixmap to display the icon
        pixmap = load_pixmap_icon(icon_name)
        # Set the pixmap to the label
        self.lbl_icon.setPixmap(
            pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        )

    def set_button_configuration(self, buttons):
        """Set the buttons to display on the dialog box."""
        self.button_box.setStandardButtons(buttons)

class OkDialogBoxView(LabelIconDialog):
    """A simple dialog box with an OK button."""

    def __init__(
        self, message: str = "Complete", title: str = "Action Complete", parent=None
    ):
        super().__init__(parent)
        self.set_button_configuration(QDialogButtonBox.StandardButton.Ok)
        self.set_icon("ok-icon.png")
        self.message = message
        self.title = title

class ErrorDialogBoxView(LabelIconDialog):
    """A dialog box to display an error message."""

    def __init__(
        self, message: str = "An error occurred.", title: str = "Error", parent=None
    ):
        super().__init__(parent)
        self.set_button_configuration(QDialogButtonBox.StandardButton.Ok)
        self.set_icon("error-icon.png")
        self.message = message
        self.title = title

class ConfirmDialogBoxView(LabelIconDialog):
    """A dialog box to confirm an action."""

    def __init__(
        self, message: str = "Are you sure?", title: str = "Confirm", parent=None
    ):
        super().__init__(parent)
        self.set_button_configuration(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.set_icon("question-icon.png")
        self.message = message
        self.title = title

class YesNoDialogBoxView(LabelIconDialog):
    """A dialog box to make a Yes/No decision."""

    def __init__(
        self, message: str = "Are you sure?", title: str = "Confirm", parent=None
    ):
        super().__init__(parent)
        self.set_button_configuration(
            QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No
        )
        self.set_icon("question-icon.png")
        self.message = message
        self.title = title

class EntityNameDialogView(DialogBoxView):
    """A dialog box for creating and editing the name of an entity."""

    nameChanged = pyqtSignal(str)
    nameAccepted = pyqtSignal(str)
    nameCancelled = pyqtSignal()

    def __init__(self, entity_name:str, parent=None):
        super().__init__(parent)
        self.title = f"New {entity_name.capitalize()}"

        # Add a vertical layout to the dialog
        lyt_top_level = QVBoxLayout(self)

        # Create a stacked widget to show the three labels
        self.stackedWidget = QStackedWidget()
        lyt_top_level.addWidget(self.stackedWidget)
        # Create three labels
        self.lbl_info_message = IconLabel(
            icon_filename="info-icon.png",
            text=f"Enter the {entity_name.lower()} name:"
        )
        self.lbl_name_available = IconLabel(
            icon_filename="ok-icon.png",
            text="Name is available."
        )
        self.lbl_name_unavailable = IconLabel(
            icon_filename="error-icon.png",
            text="Name is unavailable."
        )
        # Add the labels to the stacked widget
        self.stackedWidget.addWidget(self.lbl_info_message)
        self.stackedWidget.addWidget(self.lbl_name_available)
        self.stackedWidget.addWidget(self.lbl_name_unavailable)
        # Show only the instruction label
        self.show_instructions()

        # Add a textbox for the entity name
        self.txt_name = QLineEdit()
        lyt_top_level.addWidget(self.txt_name)
        # Connect the text changed signal
        self.txt_name.textChanged.connect(self.nameChanged)

        # Add a horizontal layout for buttons
        lyt_buttons = QHBoxLayout()
        lyt_top_level.addLayout(lyt_buttons)
        # Add an OK button
        self.btn_ok = ConfirmButton()
        self.btn_cancel = ClearButton()
        lyt_buttons.addWidget(self.btn_ok)
        lyt_buttons.addWidget(self.btn_cancel)
        # Connect the button signals
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    @property
    def name(self) -> str | None:
        """Returns the name if set, otherwise None."""
        if self.txt_name.text() == "":
            return None
        else:
            return self.txt_name.text()
    
    @property
    def name_is_set(self) -> bool:
        """Returns True/False to indicate if the name is set."""
        return self.name != None
    
    def show_instructions(self) -> None:
        """Show the instructions label."""
        self.stackedWidget.setCurrentWidget(self.lbl_info_message)

    def show_name_available(self) -> None:
        """Show the name available label."""
        self.stackedWidget.setCurrentWidget(self.lbl_name_available)

    def show_name_unavailable(self) -> None:
        """Show the name unavailable label."""
        self.stackedWidget.setCurrentWidget(self.lbl_name_unavailable)

    def enable_ok_button(self) -> None:
        """Enable/disable the OK button."""
        self.btn_ok.setEnabled(self.name_is_set)
    
    def disable_ok_button(self) -> None:
        """Disable the OK button."""
        self.btn_ok.setEnabled(False)

    def clear(self) -> None:
        """Clear the name text box."""
        self.txt_name.clear()
