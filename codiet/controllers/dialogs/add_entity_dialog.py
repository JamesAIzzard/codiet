from typing import Callable

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget

from codiet.utils.bidirectional_map import BidirectionalMap
from codiet.views.dialogs.add_entity_dialog_view import AddEntityDialogView
from codiet.controllers.search.search_column import SearchColumn

class AddEntityDialog(QObject):
    """Dialog to select a named entity from a list adding or inclusion.
    
    Signals:
        entityAdded: Emitted when an entity is added. The signal is emitted with
            the entity ID.
    """

    entityAdded = pyqtSignal(int)

    def __init__(
            self,
            get_entity_list: Callable[[], BidirectionalMap[int, str]],
            can_add_entity: Callable[[int], bool],
            parent: QWidget|None = None,
            view: AddEntityDialogView|None = None,
        ):
            """
            Initializes an instance of the AddEntityDialog class.

            Args:
                entity_list (BidirectionalMap[int, str]): A bidirectional map representing the entity list.
                can_add_entity (Callable[[int], bool]): A callable function that determines if an entity can be added.
                parent (QWidget|None, optional): The parent widget. Defaults to None.
                view (AddEntityDialogView|None, optional): The view for the add entity dialog. Defaults to None.
            """
            super().__init__()

            # Build the view if it is not provided
            if view is None:
                view = AddEntityDialogView(parent=parent)
            self.view = view

            # Stash the constructor arguments
            self._get_entity_list = get_entity_list
            self._can_add_entity = can_add_entity

            # Init the search column instance
            self.entity_search_column = SearchColumn(
                get_searchable_strings=lambda: self._get_entity_list().values,
                get_view_item_and_data_for_string=lambda entity_name: (
                    entity_name,
                    self._get_entity_list().get_keys(entity_name)
                ),
                view=self.view.entity_search_column
            )

            # Connect the signals
            self.view.entity_search_column.search_results.itemClicked.connect(
                lambda _, item_data: self._on_entity_selected(item_data)
            )
            self.view.btn_cancel.clicked.connect(self.view.close)
            self.view.btn_add.clicked.connect(self._on_add_button_clicked)

    def _on_entity_selected(self, entity_id: int) -> None:
        """Handles the selection of an entity.
        Uses the callback to check if the entity can be added. Enables or disables the add button accordingly.

        Args:
            entity_id (int): The ID of the selected entity.
        """
        # Check if the entity can be added and set the add button state accordingly
        if self._can_add_entity(entity_id):
            self.view.btn_add.setEnabled(True)
        else:
            self.view.btn_add.setEnabled(False)

    def _on_add_button_clicked(self) -> None:
        """Handles the add button click event.
        Emits the entityAdded signal with the selected entity ID.
        """
        # Emit the entity added signal
        self.entityAdded.emit(
            self.entity_search_column.view.search_results.selected_item_data
        )
        self.view.close()