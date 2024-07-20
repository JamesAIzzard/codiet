from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

from codiet.views.dialogs.dialog_view import DialogView
from codiet.views.buttons import AddButton, CancelButton
from codiet.views.search.search_column_view import SearchColumnView


class AddEntityDialogView(DialogView):
    """A dialog box for selecting and adding an entity.

    This class represents a dialog box that allows the user to select an entity from a list
    and add it.
    """

    entityAdded = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        """Initialise the add flag dialog view.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

        # Build the user interface
        self._build_ui()

        # Connect the signals
        self.btn_add.clicked.connect(
            lambda: self.entityAdded.emit(
                self.entity_search_column.search_results.selected_item_data
            )
        )

    def _build_ui(self):
        """Constructs the user interface."""
        # Set the top level vertical layout
        lyt_outer = QVBoxLayout()
        self.setLayout(lyt_outer)

        # Create the search column and add it to the layout
        self.entity_search_column = SearchColumnView(parent=self)
        lyt_outer.addWidget(self.entity_search_column)

        # Create a horizontal layout for the buttons
        lyt_buttons = QHBoxLayout()
        lyt_outer.addLayout(lyt_buttons)

        # Create the buttons and add them to the button layout
        self.btn_add = AddButton(parent=self)
        self.btn_cancel = CancelButton(parent=self)
        lyt_buttons.addWidget(self.btn_add)
        lyt_buttons.addWidget(self.btn_cancel)

        # Set initial state of the add button
        self.btn_add.setEnabled(False)
