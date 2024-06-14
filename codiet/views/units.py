from PyQt6.QtCore import pyqtSignal, QVariant
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QComboBox,
)

from codiet.utils.pyqt import block_signals # TODO: Update this to live in the views __init__ file.
from codiet.views import load_stylesheet
from codiet.views.labels import IconTextLabel
from codiet.views.buttons import AddButton, RemoveButton, EditButton
from codiet.views.text_editors import NumericLineEdit
from codiet.views.listbox import ListBox


class CustomUnitView(QWidget):
    """A widget for defining a custom unit."""

    customUnitQtyChanged = pyqtSignal(str, QVariant)
    stdUnitQtyChanged = pyqtSignal(str, QVariant)
    stdUnitChanged = pyqtSignal(str, str)

    def __init__(self, unit_id:int, unit_name:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._unit_id = unit_id
        self._unit_name = unit_name
        self.build_ui()
        self.setStyleSheet(load_stylesheet("custom_unit_view.qss"))

    @property
    def unit_id(self) -> int:
        """Return the unit ID."""
        return self._unit_id

    @property
    def unit_name(self) -> str:
        """Return the name of the quantity."""
        return self._unit_name
    
    @unit_name.setter
    def unit_name(self, name: str) -> None:
        """Set the name of the quantity."""
        self._unit_name = name
        self.lbl_icon.text = f"{self._unit_name}: "
        self.lbl_unit_name.setText(f"{self.unit_name} = ")

    @property
    def custom_unit_qty(self) -> float | None:
        """Return the custom unit quantity."""
        return self.txt_custom_unit_qty.text()
    
    @custom_unit_qty.setter
    def custom_unit_qty(self, value: float | None) -> None:
        """Set the custom unit quantity."""
        with block_signals(self.txt_custom_unit_qty):
            self.txt_custom_unit_qty.setText(value)

    @property
    def std_unit_qty(self) -> float | None:
        """Return the standard unit quantity."""
        return self.txt_std_unit_qty.text()
    
    @std_unit_qty.setter
    def std_unit_qty(self, value: float | None) -> None:
        """Set the standard unit quantity."""
        with block_signals(self.txt_std_unit_qty):
            self.txt_std_unit_qty.setText(value)

    @property
    def std_unit_name(self) -> str:
        """Return the standard unit."""
        return self.cmb_std_unit.currentText()
    
    @std_unit_name.setter
    def std_unit_name(self, value: str) -> None:
        """Set the standard unit."""
        with block_signals(self.cmb_std_unit):
            self.cmb_std_unit.setCurrentText(value)

    def build_ui(self):
        """Constructs the user interface."""
        # Create a top level horizontal layout
        layout = QHBoxLayout()
        self.setLayout(layout)
        # Remove margins
        layout.setContentsMargins(0, 0, 0, 0)
        # Add a label with the weight icon
        self.lbl_icon = IconTextLabel(
            icon_filename="weight-icon.png", text=f"{self._unit_name}: "
        )
        # Set a fixed width
        self.lbl_icon.setFixedWidth(100)
        layout.addWidget(self.lbl_icon)
        # Add a numeric line edit
        self.txt_custom_unit_qty = NumericLineEdit()
        self.txt_custom_unit_qty.setFixedWidth(60)
        layout.addWidget(self.txt_custom_unit_qty)
        self.txt_custom_unit_qty.lostFocus.connect(
            lambda: self.customUnitQtyChanged.emit(
                self._unit_name, self.txt_custom_unit_qty.text
            )
        )
        # Add a label with the quantity name
        self.lbl_unit_name = QLabel(f"{self._unit_name} = ")
        self.lbl_unit_name.setFixedWidth(100)
        layout.addWidget(self.lbl_unit_name)
        # Add a numeric line edit for the standard unit quantity
        self.txt_std_unit_qty = NumericLineEdit()
        self.txt_std_unit_qty.setFixedWidth(60)
        layout.addWidget(self.txt_std_unit_qty)
        self.txt_std_unit_qty.lostFocus.connect(
            lambda: self.stdUnitQtyChanged.emit(
                self._unit_name, self.txt_std_unit_qty.text
            )
        )
        # Add a combo box for the standard unit
        self.cmb_std_unit = QComboBox()
        layout.addWidget(self.cmb_std_unit)
        # TODO: Add standard units from database, but add a few for now
        self.cmb_std_unit.addItems(["g", "kg", "lb", "oz"])
        self.cmb_std_unit.currentTextChanged.connect(
            lambda: self.stdUnitChanged.emit(
                self._unit_name, self.cmb_std_unit.currentText()
            )
        )
        # Add a spacer to push the combo box to the right
        layout.addStretch()


class CustomUnitsDefinitionView(QWidget):
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
