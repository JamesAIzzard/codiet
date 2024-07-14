from typing import Callable, Optional

from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QWidget

from codiet.utils.map import IntStrMap
from codiet.views.flags.add_flag_dialog_view import AddFlagDialogView
from codiet.controllers.search.search_column import SearchColumn

class AddFlagDialog(QObject):
    """Controller for the add flag dialog view.
    This controller is responsible for managing the addition of flags to
    entities in the application.

    Signals:
        flagAdded: Emitted when a flag is added. The signal is emitted with
            the flag ID.
    """

    flagAdded = pyqtSignal(int)

    def __init__(
        self,
        global_flags: IntStrMap,
        can_add_flag: Callable[[int], bool],
        view: Optional[AddFlagDialogView] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        """Initialise the controller.

        Args:
            global_flags: A dictionary of flag IDs and their names.
            can_add_flag: A callback that returns whether a flag can be added
                to the current entity.
            view: The view to use for the add flag dialog. If not provided, a
                new view will be created.
            parent: The parent widget for the view.
        """
        super().__init__()

        # Build the view if it is not provided
        if view is None:
            view = AddFlagDialogView(parent=parent)
        self.view = view

        # Stash the constructor arguments
        self._global_flags = global_flags
        self._can_add_flag = can_add_flag

        # Init the search column instance
        self.flag_search_column = SearchColumn(
            get_searchable_strings=lambda: self._global_flags.str_values,
            get_view_item_and_data_for_string=lambda flag_name: (
                flag_name,
                self._global_flags.get_int(flag_name)
            ),
            view=self.view.flag_search_column,
        )

        # Connect the signals
        self.view.flagSelected.connect(self._on_flag_selected)
        self.view.cancelClicked.connect(self.view.close)
        self.view.flagAdded.connect(lambda flag_id: self.flagAdded.emit(flag_id))

    def _on_flag_selected(self, flag_id: int) -> None:
        """Handle a flag being selected in the dialog.

        Args:
            flag_id (int): The ID of the selected flag.

        Returns:
            None

        """
        # Set the enabled state of the add button
        self.view.btn_add.setEnabled(self._can_add_flag(flag_id))