from PyQt6.QtCore import pyqtSignal

from typing import Callable

from codiet.views.entity_name_editor_view import EntityNameEditorView
from codiet.controllers.base_controller import BaseController
from codiet.controllers.dialogs import EntityNameEditorDialog

class EntityNameEditor(BaseController[EntityNameEditorView]):
    """Controller for the entity name editor."""

    nameChanged = pyqtSignal(str)

    def __init__(
            self,
            entity_type_name:str,
            get_entity_name: Callable[[], str|None],
            check_name_available: Callable[[str], bool],
            *args, **kwargs
        ):
        """Initialise the entity name editor."""
        super().__init__(*args, **kwargs)

        self._get_entity_name = get_entity_name

        # Init the name editor dialog
        self.name_editor_dialog = EntityNameEditorDialog(
            parent=self.view,
            entity_type_name=entity_type_name,
            check_name_available=check_name_available
        )
        # Change the text to represent edit use case
        self.name_editor_dialog.view.title = f"Edit {entity_type_name.capitalize()} Name"
        self.name_editor_dialog.view.set_info_message(f"Enter new {entity_type_name} name.")
        
        # When accept is pressed, emit the signal
        self.name_editor_dialog.onNameAccepted.connect(self.nameChanged)

        # When the edit button is pressed, open the dialog.
        self.view.btn_edit.clicked.connect(self._on_edit_name_clicked)
        
    @property
    def entity_name(self) -> str|None:
        """Return the entity name."""
        return self.view.txt_ingredient_name.text()
    
    @entity_name.setter
    def entity_name(self, name: str|None) -> None:
        """Set the entity name."""
        self.view.txt_ingredient_name.setText(name)

    def refresh(self) -> None:
        """Refresh the entity name editor."""
        self.view.txt_ingredient_name.setText(self._get_entity_name())

    def _on_edit_name_clicked(self) -> None:
        """Clears the name editor dialog and shows it."""
        self.name_editor_dialog.clear()
        self.name_editor_dialog.show()

    def _create_view(self, *args, **kwargs) -> EntityNameEditorView:
        return EntityNameEditorView(*args, **kwargs)