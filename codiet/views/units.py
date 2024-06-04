from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QComboBox
)

from codiet.views import load_stylesheet
from codiet.views.buttons import AddButton, RemoveButton, EditButton
from codiet.views.text_editors import NumericLineEdit
from codiet.views.listbox import ListBox

class CustomUnitsDefinitionView(QWidget):
    """A widget for defining custom measurement units."""
    addMeasurementClicked = pyqtSignal()
    removeMeasurementClicked = pyqtSignal(str)
    editMeasurementClicked = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build_ui()
        
    def build_ui(self):
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
        # TODO: Connect remove button, providing custom unit name
        self.btn_edit = EditButton()
        lyt_buttons.addWidget(self.btn_edit)
        # TODO: Connect edit button, providing custom unit name
        # Drop in a spacer to push buttons to lhs
        lyt_buttons.addStretch()
        # Add a listbox of custom measurements
        self.lst_measurements = ListBox()
        lyt_top_level.addWidget(self.lst_measurements)


class CustomUnitView(QWidget):
    """A widget for defining a custom unit."""
    customQtyValueChanged = pyqtSignal(str, float)
    stdQtyValueChanged = pyqtSignal(str, float)
    stdQtyUnitChanged = pyqtSignal(str, str)

    def __init__(self, qty_name:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quantity_name = qty_name
        self.build_ui()
        self.setStyleSheet(load_stylesheet("custom_unit_view.qss"))
        
    def build_ui(self):
        """Constructs the user interface."""
        # Create a top level horizontal layout
        layout = QHBoxLayout()
        self.setLayout(layout)
        # Remove margins
        layout.setContentsMargins(0, 0, 0, 0)
        # Add a label with the quantity name
        self.lbl_qty_name = QLabel(f"{self.quantity_name}:")
        # Give it a class of unit-title
        self.lbl_qty_name.setProperty("class", "unit-title")
        layout.addWidget(self.lbl_qty_name)
        # Add a numeric line edit
        self.txt_custom_unit_qty = NumericLineEdit()
        layout.addWidget(self.txt_custom_unit_qty)
        self.txt_custom_unit_qty.lostFocus.connect(
            lambda: self.customQtyValueChanged.emit(
                self.quantity_name, 
                self.txt_custom_unit_qty.text
            )
        )
        # Add a label with the quantity name
        self.lbl_qty_name = QLabel(f"{self.quantity_name} weighs  ")
        layout.addWidget(self.lbl_qty_name)
        # Add a numeric line edit for the standard unit quantity
        self.txt_std_unit_qty = NumericLineEdit()
        layout.addWidget(self.txt_std_unit_qty)
        self.txt_std_unit_qty.lostFocus.connect(
            lambda: self.stdQtyValueChanged.emit(
                self.quantity_name, 
                self.txt_std_unit_qty.text
            )
        )
        # Add a combo box for the standard unit
        self.cmb_std_unit = QComboBox()
        layout.addWidget(self.cmb_std_unit)
        # TODO: Add standard units from database, but add a few for now
        self.cmb_std_unit.addItems(["g", "kg", "lb", "oz"])
        self.cmb_std_unit.currentTextChanged.connect(
            lambda: self.stdQtyUnitChanged.emit(
                self.quantity_name, 
                self.cmb_std_unit.currentText()
            )
        )

        