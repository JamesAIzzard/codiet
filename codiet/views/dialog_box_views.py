from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QStackedWidget
)

from codiet.utils.pyqt import block_signals
from codiet.views import load_icon
from codiet.views.text_editors import LineEdit
from codiet.views.buttons import ConfirmButton, ClearButton, OKButton
from codiet.views.labels import IconTextLabel

class DialogBoxView(QDialog):
    """A base class for dialog boxes with the codiet logo."""
    def __init__(self, title:str = "Title", parent=None):
        super().__init__(parent=parent)

        # Set the window title
        self.setWindowTitle(title)
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

class LabelIconButtonsDialog(LabelIconDialog):
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

class OkDialogBoxView(LabelIconButtonsDialog):
    """A simple dialog box with an OK button."""

    okClicked = pyqtSignal()

    def __init__(self, title="OK", message="OK", *args, **kwargs):
        super().__init__(title=title, message=message, *args, **kwargs)
        # Add the button
        self.btn_ok = self.add_button(OKButton())
        # Connect the button to the signal
        self.btn_ok.clicked.connect(self.okClicked)

class ErrorDialogBoxView(OkDialogBoxView):
    """A dialog box to display an error message."""

    def __init__(self, title="Error", message="An error occurred.", *args, **kwargs):
        super().__init__(title=title, message=message, *args, **kwargs)
        self.set_icon("error-icon.png")

class ConfirmDialogBoxView(LabelIconButtonsDialog):
    """A dialog box to confirm an action."""

    confirmClicked = pyqtSignal()
    cancelClicked = pyqtSignal()

    def __init__(self, title="Confirm", message="Are you sure?", *args, **kwargs):
        super().__init__(title=title, message=message, icon_filename="question-icon.png", *args, **kwargs)
        self.btn_confirm = self.add_button(ConfirmButton())
        self.btn_clear = self.add_button(ClearButton())
        self.btn_confirm.clicked.connect(self.confirmClicked)
        self.btn_clear.clicked.connect(self.cancelClicked)

class EntityNameDialogView(DialogBoxView):
    """A dialog box for creating and editing the name of an entity."""

    nameChanged = pyqtSignal(str)
    nameAccepted = pyqtSignal(str)
    nameCancelled = pyqtSignal()

    def __init__(self, entity_name:str, *args, **kwargs):
        super().__init__(
            title=f"New {entity_name.capitalize()}",
            *args, **kwargs
        )

        # Set the width of the dialog
        self.setFixedWidth(350)

        # Add a vertical layout to the dialog
        lyt_top_level = QVBoxLayout(self)

        # Create a stacked widget to show the three labels
        self.stackedWidget = QStackedWidget()
        lyt_top_level.addWidget(self.stackedWidget)
        # Create three labels
        self.lbl_info_message = IconTextLabel(
            icon_filename="info-icon.png",
            text=f"Enter the {entity_name.lower()} name."
        )
        self.lbl_name_available = IconTextLabel(
            icon_filename="ok-icon.png",
            text="Name is available."
        )
        self.lbl_name_unavailable = IconTextLabel(
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
        self.txt_name = LineEdit()
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
        # When the buttons are clicked, emit the signals
        self.btn_ok.clicked.connect(
            lambda: self.nameAccepted.emit(self.txt_name.text())
        )
        self.btn_cancel.clicked.connect(self.nameCancelled)

    @property
    def name(self) -> str | None:
        """Returns the name if set, otherwise None."""
        if self.txt_name.text() == "":
            return None
        else:
            return self.txt_name.text()
    
    @name.setter
    def name(self, name: str):
        """Set the name in the text box."""
        with block_signals(self.txt_name):
            self.txt_name.setText(name)

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