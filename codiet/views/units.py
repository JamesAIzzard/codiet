from PyQt6.QtCore import pyqtSignal, QVariant
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QComboBox,
)

from codiet.views import block_signals
from codiet.views import load_stylesheet
from codiet.views.dialog_box_views import DialogBoxView
from codiet.views.labels import IconTextLabel
from codiet.views.buttons import AddButton, RemoveButton, EditButton, OKButton, CancelButton
from codiet.views.text_editors import NumericLineEdit
from codiet.views.listbox import ListBox
from codiet.views.search import SearchColumnView

class UnitDropdown(QComboBox):
    """A widget for selecting units."""

    unitChanged = pyqtSignal(QVariant)

    def __init__(self, *args, **kwargs):
        """Initialise the standard unit editor view."""
        super().__init__(*args, **kwargs)
        # When the combo box changes, emit the signal containing the
        # global id of the unit, which was stored in the userdata
        self.currentTextChanged.connect(
            lambda: self.unitChanged.emit(
                self.currentData()
            )
        )

    @property
    def selected_unit_id(self) -> int | None:
        """Return the selected unit ID.
        Args:
            None
        Returns:
            int | None: The global ID of the unit.
        """
        return self.currentData()
    
    @selected_unit_id.setter
    def selected_unit_id(self, unit_id: int | None) -> None:
        """Set the selected unit ID.
        If the unit ID is none, select the first item in the combo box.
        Args:
            unit_id (int | None): The global ID of the unit.
        Returns:
            None
        """
        with block_signals(self):
            if unit_id is not None:
                idx = self.findData(unit_id)
                self.setCurrentIndex(idx)
            else:
                self.setCurrentIndex(0)

    def add_unit(self, unit_display_name: str, unit_global_id:int|None) -> None:
        """Add a unit to the combo box.
        Args:
            unit_display_name (str): The display name of the unit.
            unit_global_id (int|None): The global ID of the unit.
        Returns:
            None
        """
        self.addItem(unit_display_name, unit_global_id)

    def clear_units(self) -> None:
        """Clear all units from the combo box.
        Args:
            None
        Returns:
            None
        """
        # Clear existing
        self.clear()

    def add_units(self, units: dict[int|None, str]) -> None:
        """Add a dictionary of units to the combo box.
        Args:
            units (dict[int|None, str]): A dictionary of units where the key is the
                global ID of the unit and the value is the display name.
        Returns:
            None
        """
        for unit_global_id, unit_display_name in units.items():
            self.add_unit(unit_display_name, unit_global_id)

    def remove_unit(self, unit_global_id: int) -> None:
        """Remove a unit from the combo box.
        Args:
            unit_global_id (int): The global ID of the unit.
        Returns:
            None
        """
        # Find the unit index based on the unit_global_id
        unit_index = self.findData(unit_global_id)
        if unit_index != -1:
            # Remove the unit
            self.removeItem(unit_index)
        
    def update_unit(self, unit_display_name: str, unit_global_id: int) -> None:
        """Update the display name of a unit.
        Args:
            unit_display_name (str): The new display name.
            unit_global_id (int): The global ID of the unit.
        Returns:
            None
        """
        # Find the unit index based on the unit_global_id
        unit_index = self.findData(unit_global_id)
        if unit_index != -1:
            # Update the unit display name
            self.setItemText(unit_index, unit_display_name)

class StandardUnitEditorView(QWidget):
    """A widget for editing the standard unit of an ingredient."""

    def __init__(self, *args, **kwargs):
        """Initialise the standard unit editor view."""
        super().__init__(*args, **kwargs)
        self._build_ui()

    def _build_ui(self):
        """Constructs the user interface."""
        # Create a horizontal layout
        layout = QHBoxLayout()
        self.setLayout(layout)
        # Create a label
        lbl_standard_unit = QLabel("Standard Unit:")
        layout.addWidget(lbl_standard_unit)
        # Create unit editor
        self.cmb_standard_unit = UnitDropdown()
        layout.addWidget(self.cmb_standard_unit)
        # Add a spacer to push the combo box to the LHS
        layout.addStretch()

class UnitConversionEditorView(QWidget):
    """A widget for editing a unit conversion."""

    fromUnitQtyChanged = pyqtSignal(QVariant)
    toUnitQtyChanged = pyqtSignal(QVariant)

    def __init__(self,
            id: int,
            from_unit_id:int, 
            to_unit_id:int,
            from_unit_display_name: str,
            to_unit_display_name: str,
            *args, **kwargs
        ):
        """Initialise the unit conversion editor view."""
        super().__init__(*args, **kwargs)
        self.id = id
        self.from_unit_id = from_unit_id
        self.to_unit_id = to_unit_id
        self.from_unit_display_name = from_unit_display_name
        self.to_unit_display_name = to_unit_display_name
        self._build_ui()

    def _build_ui(self):
        """Constructs the user interface."""
        # Create a horizontal layout
        layout = QHBoxLayout()
        self.setLayout(layout)
        # Create a numeric box for the from unit quantity
        self.txt_from_unit_qty = NumericLineEdit()
        layout.addWidget(self.txt_from_unit_qty)
        # Create a label for the from unit
        lbl_from_unit = QLabel(self.from_unit_display_name)
        # Create a label for the equals sign
        lbl_equals = QLabel(" = ")
        layout.addWidget(lbl_equals)
        # Create a numeric box for the to unit quantity
        self.txt_to_unit_qty = NumericLineEdit()
        layout.addWidget(self.txt_to_unit_qty)
        # Create a label for the to unit
        lbl_to_unit = QLabel(self.to_unit_display_name)
        # Add a spacer to push the combo box to the LHS
        layout.addStretch()

class UnitConversionsEditorView(QWidget):
    """A widget for defining custom measurement units."""

    addUnitClicked = pyqtSignal()
    removeUnitClicked = pyqtSignal(QVariant)
    editUnitClicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build_ui()

    @property
    def selected_unit_view(self) -> CustomUnitView | None:
        """Return the selected custom measurement view."""
        if not self.lst_measurements.item_is_selected:
            return None
        else:
            # Grab the list widget item
            item = self.lst_measurements.selected_item
            # Grab the widget from the item
            custom_unit_view: CustomUnitView = self.lst_measurements.itemWidget(item)  # type: ignore
            # Return the widget
            return custom_unit_view

    @property
    def selected_unit_id(self) -> int | None:
        """Return the ID of the selected custom measurement."""
        if self.selected_unit_view is not None:
            return self.selected_unit_view.unit_id

    @property
    def selected_unit_name(self) -> str | None:
        """Return the name of the selected custom measurement."""
        if self.selected_unit_view is not None:
            return self.selected_unit_view.unit_name

    def change_unit_name(self, unit_id: int, new_name: str) -> None:
        """Change the name of a unit."""
        # Grab the item with the old name
        for i in range(self.lst_measurements.count()):
            item = self.lst_measurements.item(i)
            custom_unit_view: CustomUnitView = self.lst_measurements.itemWidget(item)  # type: ignore
            if custom_unit_view.unit_id == unit_id:
                # Set the new name
                custom_unit_view.unit_name = new_name
                break

    def _on_remove_unit_clicked(self):
        """Called when the remove unit button is clicked."""
        # If nothing is selected, emit signal with None
        if not self.lst_measurements.item_is_selected:
            self.removeUnitClicked.emit(None)
        else:
            # Emit the signal with the name of the selected measurement
            self.removeUnitClicked.emit(self.selected_unit_name)

    def _build_ui(self):
        """Constructs the user interface."""
        # Create a vertical layout for the widget
        lyt_outer = QVBoxLayout()
        self.setLayout(lyt_outer)
        lyt_outer.setContentsMargins(0, 0, 0, 0)
        # Put a groupbox inside
        grp_measurements = QGroupBox("Custom Measurements")
        lyt_outer.addWidget(grp_measurements)
        # Create a vertical layout for the groupbox
        lyt_top_level = QVBoxLayout()
        grp_measurements.setLayout(lyt_top_level)
        # Create a horizontal layout for the buttons
        lyt_buttons = QHBoxLayout()
        lyt_top_level.addLayout(lyt_buttons)
        # Add the buttons
        self.btn_add = AddButton()
        lyt_buttons.addWidget(self.btn_add)
        self.btn_add.clicked.connect(self.addUnitClicked.emit)
        self.btn_remove = RemoveButton()
        lyt_buttons.addWidget(self.btn_remove)
        self.btn_remove.clicked.connect(self._on_remove_unit_clicked)
        self.btn_edit = EditButton()
        lyt_buttons.addWidget(self.btn_edit)
        self.btn_edit.clicked.connect(self.editUnitClicked.emit)
        # Drop in a spacer to push buttons to lhs
        lyt_buttons.addStretch()
        # Add a listbox of custom measurements
        self.lst_measurements = ListBox()
        lyt_top_level.addWidget(self.lst_measurements)

class UnitConversionDefinitionPopupView(DialogBoxView):
    """A dialog box for defining a unit conversion."""
    selectionChanged = pyqtSignal(int, int)
    OKClicked = pyqtSignal(int, int)
    cancelClicked = pyqtSignal()

    def __init__(
        self,
        *args, **kwargs
    ):
        """Initialise the unit conversion definition popup view."""
        super().__init__(*args, **kwargs)
        self._build_ui()
        # Connect the signals
        self.from_unit_selector.resultClicked.connect(self._on_selection_changed)
        self.to_unit_selector.resultClicked.connect(self._on_selection_changed)
        self.btn_ok.clicked.connect(self._on_OK_clicked)
        self.btn_cancel.clicked.connect(self.cancelClicked.emit)

    @property
    def selected_from_unit_id(self) -> int:
        """Return the selected from unit ID.
        Returns:
            int: The global ID of the selected from unit.
        """
        return self.from_unit_selector.lst_search_results.selected_item_data
    
    @property
    def selected_to_unit_id(self) -> int | None:
        """Return the selected to unit ID."""
        return self.to_unit_selector.lst_search_results.selected_item_data

    def _on_selection_changed(self) -> None:
        """Called when the selection is changed."""
        # Emit the OKClicked signal with the from and to unit IDs
        self.selectionChanged.emit(
            self.from_unit_selector.lst_search_results.selected_item_data, 
            self.to_unit_selector.lst_search_results.selected_item_data
        )

    def _on_OK_clicked(self) -> None:
        """Called when the OK button is clicked."""
        # Emit the OKClicked signal with the from and to unit IDs
        self.OKClicked.emit(
            self.from_unit_selector.lst_search_results.selected_item_data,
            self.to_unit_selector.lst_search_results.selected_item_data
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
        self.btn_ok = OKButton()
        lyt_buttons.addWidget(self.btn_ok)
        # Create a Cancel button
        self.btn_cancel = CancelButton()
        lyt_buttons.addWidget(self.btn_cancel)
        
