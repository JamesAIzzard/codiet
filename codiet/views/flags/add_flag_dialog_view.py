from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

from codiet.views.dialogs.dialog_view import DialogView
from codiet.views.buttons import AddButton, CancelButton
from codiet.views.search.search_column_view import SearchColumnView


class AddFlagDialogView(DialogView):
    """A dialog box for adding a flag to an entity.

    This class represents a dialog box that allows the user to add a flag to an entity.
    It inherits from the `DialogView` class.

    Signals:
        flagSelected: This signal is emitted when a flag is selected.
        flagAdded: This signal is emitted when a flag is added.
        cancelClicked: This signal is emitted when the cancel button is clicked.

    Attributes:
        btn_add: An instance of the `AddButton` class representing the add button.
        btn_cancel: An instance of the `CancelButton` class representing the cancel button.
        flag_search_column: An instance of the `SearchColumnView` class representing the search column.

    Methods:
        __init__: Initializes the `AddFlagDialogView` object.
        _build_ui: Constructs the user interface of the dialog box.
    """

    flagSelected = pyqtSignal(int)
    flagAdded = pyqtSignal(int)
    cancelClicked = pyqtSignal()

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
            lambda: self.flagAdded.emit(
                self.flag_search_column.lst_search_results.selected_item_data
            )
        )
        self.btn_cancel.clicked.connect(self.cancelClicked.emit)

    def _build_ui(self):
        """Constructs the user interface."""
        # Set the top level vertical layout
        lyt_outer = QVBoxLayout()
        self.setLayout(lyt_outer)

        # Create the search column and add it to the layout
        self.flag_search_column = SearchColumnView(parent=self)
        lyt_outer.addWidget(self.flag_search_column)

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
