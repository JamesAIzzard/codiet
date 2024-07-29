from typing import Callable

from PyQt6.QtCore import pyqtSignal

from codiet.views.dialogs.entity_name_editor_dialog_view import EntityNameEditorDialogView
from codiet.controllers.dialogs.base_dialog import BaseDialog

class EntityNameEditorDialog(BaseDialog[EntityNameEditorDialogView]):
    """A controller for the entity name dialog."""

    onNameAccepted = pyqtSignal(str)

    def __init__(
            self,
            entity_type_name:str,
            check_name_available:Callable[[str], bool],
            *args, **kwargs   
    ):
        super().__init__(entity_name=entity_type_name, *args, **kwargs)
        
        # Stash constructor arguments
        self._check_name_available = check_name_available

        # Connect signals and slots
        self.view.txt_name.textChanged.connect(self._on_name_changed)
        self.view.btn_ok.clicked.connect(self._on_name_accepted)
        self.view.btn_cancel.clicked.connect(self._on_name_edit_cancelled)

        # On initialisation, show the instructions, clear the box and disable the OK button
        self.view.show_instructions()
        self.view.txt_name.clear()
        self.view.txt_name.setEnabled(True)

    def clear(self) -> None:
        """Clear the dialog."""
        self.view.txt_name.clear()
        self.view.show_instructions()
        self.view.txt_name.setEnabled(True)

    def _create_view(self, *args, **kwargs) -> EntityNameEditorDialogView:
        return EntityNameEditorDialogView(*args, **kwargs)

    def _on_name_changed(self, name: str) -> None:
        """Handler for changes to the name."""
        # If the name is not whitespace
        if self.view.name_is_set:
            # Check if the name is in the cached list of ingredient names
            if not self._check_name_available(name):
                # Show the name unavailable message
                self.view.show_name_unavailable()
                # Disable the OK button
                self.view.btn_ok.setEnabled(False)
            else:
                # Show the name available message
                self.view.show_name_available()
                # Enable the OK button
                self.view.btn_ok.setEnabled(True)
        else:
            # Show the instructions message
            self.view.show_instructions()
            # Disable the OK button
            self.view.btn_ok.setEnabled(False)

    def _on_name_accepted(self) -> None:
        """Handler for accepting the new ingredient name."""
        # Emit the signal with the name
        self.onNameAccepted.emit(self.view.entity_name)
        # Clear the new ingredient dialog
        self.view.txt_name.clear()
        # Hide the new ingredient dialog
        self.view.hide()

    def _on_name_edit_cancelled(self) -> None:
        """Handler for cancelling the new ingredient name."""
        # Clear the new ingredient dialog
        self.view.txt_name.clear()
        # Hide the new ingredient dialog
        self.view.hide()            