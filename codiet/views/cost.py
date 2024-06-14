from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QComboBox
)
from PyQt6.QtCore import pyqtSignal, QVariant

from codiet.utils.pyqt import block_signals
from codiet.views.text_editors import NumericLineEdit

class CostEditorView(QWidget):
    """The UI element to allow the user to edit costs."""

    costChanged = pyqtSignal(QVariant, QVariant, str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build_ui()

    @property
    def cost_value(self) -> float|None:
        """Return the cost of the ingredient."""
        return self.txt_cost.text()
    
    @cost_value.setter
    def cost_value(self, value: float|None) -> None:
        """Set the cost of the ingredient."""
        with block_signals(self.txt_cost):
            self.txt_cost.setText(value)

    @property
    def cost_quantity_value(self) -> float|None:
        """Return the quantity of the ingredient."""
        return self.txt_cost_quantity_value.text()
    
    @cost_quantity_value.setter
    def cost_quantity_value(self, value: float|None) -> None:
        """Set the quantity of the ingredient."""
        with block_signals(self.txt_cost_quantity_value):
            self.txt_cost_quantity_value.setText(value)

    @property
    def cost_quantity_unit(self) -> str:
        """Return the unit of the ingredient."""
        return self.cmb_cost_qty_unit.currentText()
    
    @cost_quantity_unit.setter
    def cost_quantity_unit(self, unit: str) -> None:
        """Set the unit of the ingredient."""
        with block_signals(self.cmb_cost_qty_unit):
            self.cmb_cost_qty_unit.setCurrentText(unit)

    def _build_ui(self):
        # Create a top level layout
        lyt_top_level = QVBoxLayout()
        self.setLayout(lyt_top_level)

        # Create the cost groupbox
        gb_cost = QGroupBox("Cost")
        lyt_top_level.addWidget(gb_cost)

        # Create a horizontal layout for the cost section
        lyt_cost = QHBoxLayout()
        gb_cost.setLayout(lyt_cost)

        # Create the first label
        label = QLabel("Cost: £")
        lyt_cost.addWidget(label)

        # Create a textbox for the cost of the ingredient
        self.txt_cost = NumericLineEdit()
        lyt_cost.addWidget(self.txt_cost)
        self.txt_cost.lostFocus.connect(
            lambda: self.costChanged.emit(
                self.cost_value,
                self.cost_quantity_value,
                self.cost_quantity_unit
            )
        )

        # Create a second label
        label = QLabel(" per ")
        lyt_cost.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_cost_quantity_value = NumericLineEdit()
        lyt_cost.addWidget(self.txt_cost_quantity_value)
        self.txt_cost_quantity_value.lostFocus.connect(
            lambda: self.costChanged.emit(
                self.cost_value,
                self.cost_quantity_value,
                self.cost_quantity_unit
            )
        )

        # Create a units dropdown
        self.cmb_cost_qty_unit = QComboBox()
        # Temporarily add units, these will get pulled from config file later
        # TODO - pull units from config file
        self.cmb_cost_qty_unit.addItems(["g", "kg", "ml", "l"])
        lyt_cost.addWidget(self.cmb_cost_qty_unit)
        self.cmb_cost_qty_unit.currentTextChanged.connect(
            lambda: self.costChanged.emit(
                self.cost_value,
                self.cost_quantity_value,
                self.cost_quantity_unit
            )
        )