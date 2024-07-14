from typing import Callable

from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QWidget

from codiet.views.flag_editor_view import FlagEditorView

class FlagEditor(QObject):
    """Controller for the flag editor view.
    This controller is responsible for managing the flags associated with
    entities in the application.

    Signals:
        flagChanged: Emitted when a flag is changed. The signal is emitted
            with the flag ID and the new value of the flag.
    """

    flagChanged = pyqtSignal(int, bool|None)

    def __init__(
        self,
        get_global_flags: Callable[[], dict[int, str]],
        get_entity_flags: Callable[[], dict[int, bool|None]],
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

        # Stash the callbacks
        self._get_global_flags = get_global_flags
        self._get_entity_flags = get_entity_flags

        # Build the add flag dialog
        self.add_flag_dialog = AddFlagDialog(
            get_global_flags=self._get_global_flags,
            can_add_flag=self._can_add_flag,
            parent=self.view
        )
        self.add_flag_dialog.flagAdded.connect(self.view.add_flag)

        # Connect the flag editor signals
        self.view.flagChanged.connect(self.flagChanged.emit)
        self.view.selectAllFlagsClicked.connect(
            self._on_select_all_flags_clicked
        )
        self.view.deselectAllFlagsClicked.connect(
            self._on_deselect_all_flags_clicked
        )
        self.view.invertFlagsClicked.connect(
            self._on_invert_selection_flags_clicked
        )

    def set_flags(self, flags: dict[int, bool|None]) -> None:
        """Set the flags on the view."""
        self.view.set_flags(flags)

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
