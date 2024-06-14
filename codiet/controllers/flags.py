from typing import Callable

from codiet.views.flags import FlagEditorView

class FlagEditorCtrl:
    """Controller for the flag editor view."""

    def __init__(
        self,
        view: FlagEditorView,
        get_flags: Callable[[], dict[str, bool]],
        on_flag_changed: Callable[[str, bool], None],
    ) -> None:
        self.view = view
        self.get_flags = get_flags
        self.on_flag_changed = on_flag_changed

        # Connect the flag editor signals
        self.view.onFlagChanged.connect(self.on_flag_changed)
        self.view.onSelectAllFlagsClicked.connect(
            self._on_select_all_flags_clicked
        )
        self.view.onDeselectAllFlagsClicked.connect(
            self._on_deselect_all_flags_clicked
        )
        self.view.onInvertSelectionFlagsClicked.connect(
            self._on_invert_selection_flags_clicked
        )
        self.view.onClearSelectionFlagsClicked.connect(
            self._on_clear_selection_flags_clicked
        )

    def _on_select_all_flags_clicked(self):
        """Handler for selecting all flags."""
        # Select all flags on the view
        self.view.set_all_flags_true()
        # Call the callback for each flag
        for flag in self.get_flags():
            self.on_flag_changed(flag, True)

    def _on_deselect_all_flags_clicked(self):
        """Handler for deselecting all flags."""
        # Deselect all flags on the view
        self.view.set_all_flags_false()
        # Call the callback for each flag
        for flag in self.get_flags():
            self.on_flag_changed(flag, False)

    def _on_invert_selection_flags_clicked(self):
        """Handler for inverting the selected flags."""
        # Invert on the view
        self.view.invert_flags()
        # Call the callback for each flag
        for flag in self.get_flags():
            self.on_flag_changed(flag, not self.get_flags()[flag])

    def _on_clear_selection_flags_clicked(self):
        """Handler for clearing the selected flags."""
        # Clear all flags on the view
        self.view.set_all_flags_false()
        # Call the callback for each flag
        for flag in self.get_flags():
            self.on_flag_changed(flag, False)
