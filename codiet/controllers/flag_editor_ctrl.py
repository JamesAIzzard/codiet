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
        self.view.btn_select_all.clicked.connect(self.on_select_all_clicked)
        self.view.btn_deselect_all.clicked.connect(self.on_deselect_all_clicked)
        self.view.btn_invert_selection.clicked.connect(self.on_invert_selection_clicked)
        self.view.btn_clear_selection.clicked.connect(self.on_clear_selection)
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

    def on_select_all_clicked(self):
        """Handle the user clicking the 'Select All' button."""
        # Select all the flags on the model
        self._model.set_flags({flag: True for flag in self.flag_names})
        # Select all the flags on the view
        for flag in self.flag_names:
            self.view.select_flag(flag)

    def on_deselect_all_clicked(self):
        """Handle the user clicking the 'Deselect All' button."""
        # Deselect all the flags on the model
        self._model.set_flags({flag: False for flag in self.flag_names})
        # Deselect all the flags on the view
        for flag in self.flag_names:
            self.view.deselect_flag(flag)

    def on_invert_selection_clicked(self):
        """Handle the user clicking the 'Invert Selection' button."""
        # Grab the flags from the model
        flags = self._model.flags
        for flag in flags.keys():
            # Invert the selection of the flag
            self._model.set_flags({flag: not flags[flag]})
            if flags[flag]:
                self.view.deselect_flag(flag)
            else:
                self.view.select_flag(flag)

    def on_clear_selection(self):
        """Handle the user clicking the 'Clear Selection' button."""
        # Clear all the flags on the model
        self._model.set_flags({flag: False for flag in self.flag_names})
        # Deselect all the flags on the view
        self.view.deselect_all_flags()

    def on_flag_changed(self, item: QListWidgetItem):
        """Handle the user changing the selection of a flag."""
        flag = item.text().lower()
        selected = item.checkState() == Qt.CheckState.Checked
        self._model.set_flags({flag: selected})