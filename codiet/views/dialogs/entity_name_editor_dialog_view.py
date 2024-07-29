from PyQt6.QtWidgets import QVBoxLayout, QStackedWidget, QHBoxLayout

from codiet.views import block_signals
from codiet.views.dialogs.base_dialog_view import BaseDialogView
from codiet.views.labels import IconTextLabel
from codiet.views.icon_button import IconButton
from codiet.views.text_editors.line_editor import LineEditor

class EntityNameEditorDialogView(BaseDialogView):
    """A dialog box for creating and editing the name of an entity."""

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
        self.txt_name = LineEditor()
        lyt_top_level.addWidget(self.txt_name)

        # Add a horizontal layout for buttons
        lyt_buttons = QHBoxLayout()
        lyt_top_level.addLayout(lyt_buttons)
        # Add an OK button
        self.btn_ok = IconButton(icon_filename="ok-icon.png")
        self.btn_cancel = IconButton(icon_filename="cancel-icon.png")
        lyt_buttons.addWidget(self.btn_ok)
        lyt_buttons.addWidget(self.btn_cancel)

    @property
    def entity_name(self) -> str | None:
        """Returns the name if set, otherwise None."""
        if self.txt_name.text() == "":
            return None
        else:
            return self.txt_name.text()
    
    @entity_name.setter
    def entity_name(self, name: str):
        """Set the name in the text box."""
        with block_signals(self.txt_name):
            self.txt_name.setText(name)

    @property
    def name_is_set(self) -> bool:
        """Returns True/False to indicate if the name is set."""
        return self.entity_name != None
    
    def set_info_message(self, message: str) -> None:
        """Set the info message."""
        self.lbl_info_message.text = message

    def set_name_available_message(self, message: str) -> None:
        """Set the name available message."""
        self.lbl_name_available.text = message

    def set_name_unavailable_message(self, message: str) -> None:
        """Set the name unavailable message."""
        self.lbl_name_unavailable.text = message

    def show_instructions(self) -> None:
        """Show the instructions label."""
        self.stackedWidget.setCurrentWidget(self.lbl_info_message)

    def show_name_available(self) -> None:
        """Show the name available label."""
        self.stackedWidget.setCurrentWidget(self.lbl_name_available)

    def show_name_unavailable(self) -> None:
        """Show the name unavailable label."""
        self.stackedWidget.setCurrentWidget(self.lbl_name_unavailable)