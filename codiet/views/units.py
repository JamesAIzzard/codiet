from PyQt6.QtCore import pyqtSignal, QVariant
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QComboBox,
)

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

    def __init__(self, qty_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quantity_name = qty_name
        self.build_ui()
        self.setStyleSheet(load_stylesheet("custom_unit_view.qss"))

    @property
    def quantity_name(self) -> str:
        """Return the name of the quantity."""
        return self._quantity_name
    
    @quantity_name.setter
    def quantity_name(self, name: str) -> None:
        """Set the name of the quantity."""
        self._quantity_name = name
        self.lbl_icon.text = f"{self._quantity_name}: "
        self.lbl_qty_name.setText(f"{self.quantity_name} = ")

    def build_ui(self):
        """Constructs the user interface."""
        # Create a top level horizontal layout
        layout = QHBoxLayout()
        self.setLayout(layout)
        # Remove margins
        layout.setContentsMargins(0, 0, 0, 0)
        # Add a label with the weight icon
        self.lbl_icon = IconTextLabel(
            icon_filename="weight-icon.png", text=f"{self._quantity_name}: "
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
                self._quantity_name, self.txt_custom_unit_qty.text
            )
        )
        # Add a label with the quantity name
        self.lbl_qty_name = QLabel(f"{self._quantity_name} = ")
        self.lbl_qty_name.setFixedWidth(100)
        layout.addWidget(self.lbl_qty_name)
        # Add a numeric line edit for the standard unit quantity
        self.txt_std_unit_qty = NumericLineEdit()
        self.txt_std_unit_qty.setFixedWidth(60)
        layout.addWidget(self.txt_std_unit_qty)
        self.txt_std_unit_qty.lostFocus.connect(
            lambda: self.stdUnitQtyChanged.emit(
                self._quantity_name, self.txt_std_unit_qty.text
            )
        )
        # Add a combo box for the standard unit
        self.cmb_std_unit = QComboBox()
        layout.addWidget(self.cmb_std_unit)
        # TODO: Add standard units from database, but add a few for now
        self.cmb_std_unit.addItems(["g", "kg", "lb", "oz"])
        self.cmb_std_unit.currentTextChanged.connect(
            lambda: self.stdUnitChanged.emit(
                self._quantity_name, self.cmb_std_unit.currentText()
            )
        )
        # Add a spacer to push the combo box to the right
        layout.addStretch()


class CustomUnitsDefinitionView(QWidget):
    """A widget for defining custom measurement units."""

    addMeasurementClicked = pyqtSignal()
    removeMeasurementClicked = pyqtSignal(QVariant)
    editMeasurementClicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build_ui()

    @property
    def selected_measurement_view(self) -> CustomUnitView | None:
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
    def selected_measurement_name(self) -> str | None:
        """Return the name of the selected custom measurement."""
        if self.selected_measurement_view is not None:
            return self.selected_measurement_view._quantity_name

    def _on_remove_measurement_clicked(self):
        """Called when the remove measurement button is clicked."""
        # If nothing is selected, emit signal with None
        if not self.lst_measurements.item_is_selected:
            self.removeMeasurementClicked.emit(None)
        else:
            # Emit the signal with the name of the selected measurement
            self.removeMeasurementClicked.emit(self.selected_measurement_name)

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
        self.btn_add.clicked.connect(self.addMeasurementClicked.emit)
        self.btn_remove = RemoveButton()
        lyt_buttons.addWidget(self.btn_remove)
        self.btn_remove.clicked.connect(self._on_remove_measurement_clicked)
        self.btn_edit = EditButton()
        lyt_buttons.addWidget(self.btn_edit)
        self.btn_edit.clicked.connect(self.editMeasurementClicked.emit)
        # Drop in a spacer to push buttons to lhs
        lyt_buttons.addStretch()
        # Add a listbox of custom measurements
        self.lst_measurements = ListBox()
        lyt_top_level.addWidget(self.lst_measurements)
