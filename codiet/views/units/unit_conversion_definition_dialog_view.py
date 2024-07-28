from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal

from codiet.views.dialogs.base_dialog_view import BaseDialogView
from codiet.views.search.search_column_view import SearchColumnView
from codiet.views.icon_button import IconButton

class UnitConversionDefinitionDialogView(BaseDialogView):
    """A dialog box for defining a unit conversion."""

    selectionChanged = pyqtSignal(int, int)
    OKClicked = pyqtSignal(int, int)
    cancelClicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        """Initialise the unit conversion definition popup view."""
        super().__init__(*args, **kwargs)
        self._build_ui()
        # Connect the signals
        # self.from_unit_selector.resultClicked.connect(self._on_selection_changed)
        # self.to_unit_selector.resultClicked.connect(self._on_selection_changed)
        self.btn_ok.clicked.connect(self._on_OK_clicked)
        self.btn_cancel.clicked.connect(self.cancelClicked.emit)

    def _on_selection_changed(self) -> None:
        """Called when the selection is changed."""
        # Emit the OKClicked signal with the from and to unit IDs
        self.selectionChanged.emit(
            self.from_unit_selector.results_list_view.selected_item_data,
            self.to_unit_selector.results_list_view.selected_item_data,
        )

    def _on_OK_clicked(self) -> None:
        """Called when the OK button is clicked."""
        # Emit the OKClicked signal with the from and to unit IDs
        self.OKClicked.emit(
            self.from_unit_selector.results_list_view.selected_item_data,
            self.to_unit_selector.results_list_view.selected_item_data,
        )

    def _build_ui(self):
        """Constructs the user interface."""
        # Set the top level vertical layout
        lyt_outer = QVBoxLayout()
        self.setLayout(lyt_outer)
        # Place a horizontal layout for the selection boxes inside
        lyt_selections = QHBoxLayout()
        lyt_outer.addLayout(lyt_selections)
        # Create a vertical layout for the from unit stack
        lyt_from_unit = QVBoxLayout()
        lyt_selections.addLayout(lyt_from_unit)
        # Create a from unit label
        lbl_from_unit = QLabel("From Unit:")
        lyt_from_unit.addWidget(lbl_from_unit)
        # Create a from unit search box
        self.from_unit_selector = SearchColumnView()
        lyt_from_unit.addWidget(self.from_unit_selector)
        # Create a vertical layout for the to unit stack
        lyt_to_unit = QVBoxLayout()
        lyt_selections.addLayout(lyt_to_unit)
        # Create a to unit label
        lbl_to_unit = QLabel("To Unit:")
        lyt_to_unit.addWidget(lbl_to_unit)
        # Create a to unit search box
        self.to_unit_selector = SearchColumnView()
        lyt_to_unit.addWidget(self.to_unit_selector)
        # Create a horizontal layout for the OK and Cancel buttons
        lyt_buttons = QHBoxLayout()
        lyt_outer.addLayout(lyt_buttons)
        # Create an OK button
        self.btn_ok = IconButton(icon_filename="ok-icon.png")
        lyt_buttons.addWidget(self.btn_ok)
        # Create a Cancel button
        self.btn_cancel = IconButton(icon_filename="cancel-icon.png")
        lyt_buttons.addWidget(self.btn_cancel)
