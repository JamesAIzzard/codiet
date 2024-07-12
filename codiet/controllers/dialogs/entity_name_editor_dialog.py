from typing import Callable

from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QWidget

from codiet.views.dialogs.entity_name_editor_dialog_view import EntityNameEditorDialogView

class EntityNameEditorDialog(QObject):
    """A controller for the entity name dialog."""

    onNameAccepted = pyqtSignal(str)

    def __init__(
            self,
            entity_name:str,
            check_name_available:Callable[[str], bool],
            view: EntityNameEditorDialogView|None=None,  
            parent: QWidget|None=None      
    ):
        # Instantiate the view if not submitted
        if view is None:
            self.view = EntityNameEditorDialogView(
                parent=parent or None,
                entity_name=entity_name
            )
        else:
            self.view = view
        
        # Stash constructor arguments
        self._check_name_available = check_name_available

        # Connect signals and slots
        self.view.nameChanged.connect(self._on_name_changed)
        self.view.nameAccepted.connect(self.onNameAccepted.emit)
        self.view.nameCancelled.connect(self._on_name_edit_cancelled)

        # On initialisation, show the instructions, clear the box and disable the OK button
        self.view.show_instructions()
        self.view.clear()
        self.view.disable_ok_button()

    def _on_name_changed(self, name: str) -> None:
        """Handler for changes to the name."""
        # If the name is not whitespace
        if self.view.name_is_set:
            # Check if the name is in the cached list of ingredient names
            if not self._check_name_available(name):
                # Show the name unavailable message
                self.view.show_name_unavailable()
                # Disable the OK button
                self.view.disable_ok_button()
            else:
                # Show the name available message
                self.view.show_name_available()
                # Enable the OK button
                self.view.enable_ok_button()
        else:
            # Show the instructions message
            self.view.show_instructions()
            # Disable the OK button
            self.view.disable_ok_button()

    def _on_name_edit_cancelled(self) -> None:
        """Handler for cancelling the new ingredient name."""
        # Clear the new ingredient dialog
        self.view.clear()
        # Hide the new ingredient dialog
        self.view.hide()            