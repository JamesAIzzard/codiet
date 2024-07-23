from typing import Callable

from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QWidget

from codiet.utils.bidirectional_map import BidirectionalMap
from codiet.views.flags.flag_editor_view import FlagEditorView
from codiet.controllers.dialogs.add_entity_dialog import AddEntityDialog

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
    flagRemoved = pyqtSignal(int)

    def __init__(
        self,
        get_global_flags: Callable[[], dict[int, str]],
        get_entity_flags: Callable[[], dict[int, bool]],
        view: FlagEditorView|None=None,
        parent: QWidget|None=None,
    ) -> None:
        """Initialise the controller.
        Args:
            get_global_flags: A callable that returns a dictionary of global flags.
            get_entity_flags: A callable that returns a dictionary of entity flags.
            view: The view to use for the flag editor.
            parent: The parent widget
        """
        super().__init__()

        # Build the view if it is not provided
        if view is None:
            view = FlagEditorView(parent=parent)
        self.view = view

        # Stash the constructor args
        self._get_global_flags = get_global_flags
        self._get_entity_flags = get_entity_flags

        # Build the add flag dialog
        self.add_flag_dialog = AddEntityDialog(
            get_entity_list=lambda: BidirectionalMap(self._get_global_flags.keys(), self._get_global_flags.values()),
            can_add_entity=lambda id: id not in self._get_entity_flags().keys(),
            parent=self.view
        )
        self.add_flag_dialog.entityAdded.connect(self._on_flag_added)

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
        for flag_id, flag_value in self._get_entity_flags.items():
            self.view.add_flag(flag_id, self._get_global_flags()[flag_id])
            self.view.set_flag(flag_id, flag_value)

    def _on_flag_added(self, flag_id: int) -> None:
        """Handler for when a flag is added."""
        # Add the flag to the view
        self.view.add_flag(flag_id, self._get_global_flags()[flag_id])
        # Set the flag value to False
        self.view.set_flag(flag_id, False)
        # Emit the flagAdded signal
        self.flagAdded.emit(flag_id, False)

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
