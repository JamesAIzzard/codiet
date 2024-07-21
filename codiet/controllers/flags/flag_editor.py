from typing import Callable

from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QWidget

from codiet.utils.map import IntStrMap
from codiet.views.flags.flag_editor_view import FlagEditorView
from codiet.controllers.flags.add_flag_dialog import AddFlagDialog

class FlagEditor(QObject):
    """Controller for the flag editor view.
    This controller is responsible for managing the flags associated with
    entities in the application.

    Signals:
        flagAdded: Emitted when a flag is added.
            Arguments: flag_id (int), flag_value (bool).
        flagChanged: Emitted when a flag is changed.
            Arguments: flag_id (int), flag_value (bool).
        flag_removed: Emitted when a flag is removed.
            Arguments: flag_id (int).
    """

    flagAdded = pyqtSignal(int, bool)
    flagChanged = pyqtSignal(int, bool)
    flag_removed = pyqtSignal(int)

    def __init__(
        self,
        global_flags: IntStrMap,
        entity_flags: dict[int, bool],
        view: FlagEditorView|None=None,
        parent: QWidget|None=None,
    ) -> None:
        """Initialise the controller.
        Args:
            get_entity_flags: A callback that returns a dictionary of flag
                IDs and their values associated with the current entity.
            view: The view to use for the flag editor. If not provided, a new
                view will be created.
            parent: The parent widget for the view.
        """
        super().__init__()

        # Build the view if it is not provided
        if view is None:
            view = FlagEditorView(parent=parent)
        self.view = view

        # Stash the constructor args
        self._global_flags = global_flags
        self._entity_flags = entity_flags

        # Build the add flag dialog
        self.add_flag_dialog = AddFlagDialog(
            global_flags=self._global_flags,
            can_add_flag=lambda flag_id: flag_id not in self._entity_flags.keys(),
            parent=self.view
        )
        self.add_flag_dialog.flagAdded.connect(self.view.add_flag)

        # Connect the flag editor signals
        self.view.selectAllFlagsClicked.connect(
            self._on_select_all_flags_clicked
        )
        self.view.deselectAllFlagsClicked.connect(
            self._on_deselect_all_flags_clicked
        )
        self.view.invertFlagsClicked.connect(
            self._on_invert_selection_flags_clicked
        )

        # Add the current entity flags to the view
        for flag_id, flag_value in self._entity_flags.items():
            self.view.add_flag(flag_id, self._global_flags.get_str(flag_id))
            self.view.set_flag(flag_id, flag_value)

    def _on_select_all_flags_clicked(self):
        """Handler for selecting all flags."""
        # Select all flags on the view
        self.view.set_all_flags_true()
        # Call the callback for each flag
        for flag in self._get_entity_flags():
            self.flagChanged.emit(flag, True)

    def _on_deselect_all_flags_clicked(self):
        """Handler for deselecting all flags."""
        # Deselect all flags on the view
        self.view.set_all_flags_false()
        # Call the callback for each flag
        for flag in self._get_entity_flags():
            self.flagChanged.emit(flag, False)

    def _on_invert_selection_flags_clicked(self):
        """Handler for inverting the selected flags."""
        # Invert on the view
        self.view.invert_flags()
        # Call the callback for each flag
        for flag in self._get_entity_flags():
            self.flagChanged.emit(flag, not self._get_entity_flags()[flag])
