from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidgetItem

from codiet.views.flag_editor_view import FlagEditorView
from codiet.models.has_flags import HasSettableFlags


class FlagEditorCtrl:
    def __init__(
        self,
        view: FlagEditorView,
        model: HasSettableFlags,
    ):
        self.view = view
        self._model = model

        # Work through each flag and populate the UI list
        # Cache the flags in the model
        self.flag_names = list(
            self._model.flags.keys()
        )  # Make a copy of the keys as a list of strings
        for flag in self.flag_names:
            # Capitalise each word in the flag name
            flag = flag.title()
            self.view.add_flag_to_list(flag)

        # Connect the buttons to the controller methods
        self.view.btn_select_all.clicked.connect(self.select_all_flags)
        self.view.btn_deselect_all.clicked.connect(self.deselect_all_flags)
        self.view.btn_invert_selection.clicked.connect(self.invert_selection)
        self.view.btn_clear_selection.clicked.connect(self.clear_selection)
        self.view.lstFlagCheckboxes.itemChanged.connect(self.on_flag_changed)

    @property
    def model(self):
        return self._model

    def set_model(self, model: HasSettableFlags):
        """Set the model for the controller."""
        # Update the model reference
        self._model = model
        # Update the view with the new flags
        # First clear the old ones
        self.view.deselect_all_flags()
        # Then set flags from the new model
        for flag, value in self._model.flags.items():
            if value:
                self.view.select_flag(flag)

    def select_flag(self, flag: str) -> None:
        """Update the flag to be selected."""
        # Select the flag in the view
        self.view.select_flag(flag)
        # Select the flag in the model
        self._model.set_flags({flag: True})

    def deselect_flag(self, flag: str):
        """Update the flag to be deselected."""
        # Deselect the flag in the view
        self.view.deselect_flag(flag)
        # Deselect the flag in the model
        self._model.set_flags({flag: False})

    def select_all_flags(self):
        """Select all flags."""
        for flag in self.flag_names:
            self.select_flag(flag)

    def deselect_all_flags(self):
        """Deselect all flags."""
        for flag in self.flag_names:
            self.deselect_flag(flag)

    def invert_selection(self):
        """Invert the selection of all flags."""
        # Grab the flags from the model
        flags = self._model.flags
        for flag in flags.keys():
            # Invert the selection of the flag
            if flags[flag]:
                self.deselect_flag(flag)
            else:
                self.select_flag(flag)

    def clear_selection(self):
        """Clear the selection of all flags."""
        for flag in self.flag_names:
            self.deselect_flag(flag)

    def on_flag_changed(self, item: QListWidgetItem):
        """Handle the user changing the selection of a flag."""
        flag = item.text().lower()
        selected = item.checkState() == Qt.CheckState.Checked
        self._model.set_flags({flag: selected})