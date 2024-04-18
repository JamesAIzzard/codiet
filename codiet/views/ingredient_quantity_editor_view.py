from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox
)
from PyQt6.QtCore import Qt

from codiet.utils.pyqt import block_signals
from codiet.views.custom_line_editors import NumericLineEdit

class IngredientQuantityEditorView(QWidget):
    def __init__(self, 
            ingredient_name: str, 
            ingredient_id: int,
            ingredient_qty: float | None = None,
            ingredient_qty_unit: str = "g",
            ingredient_qty_utol: float | None = None,
            ingredient_qty_ltol: float | None = None
        ):
        super().__init__()
        
        # Stash the ingredient name
        self.ingredient_name = ingredient_name
        # Also stash the ID - this is useful for reliably identifying the ingredient
        self.ingredient_id = ingredient_id

        # Build the UI
        self._build_ui()

        # Set any values that were passed into the constructor
        if ingredient_qty is not None:
            self.set_ingredient_qty(ingredient_qty)
        self.set_ingredient_qty_unit(ingredient_qty_unit)
        if ingredient_qty_utol is not None:
            self.set_ingredient_qty_utol(ingredient_qty_utol)
        if ingredient_qty_ltol is not None:
            self.set_ingredient_qty_ltol(ingredient_qty_ltol)

    @property
    def ingredient_qty(self) -> float | None:
        """Return the ingredient quantity."""
        return self.txt_ingredient_qty.text()
    
    @property
    def ingredient_qty_unit(self) -> str:
        """Return the ingredient quantity unit."""
        return self.cmb_ingredient_qty_units.currentText()
    
    @property
    def ingredient_qty_utol(self) -> float | None:
        """Return the ingredient quantity upper tolerance."""
        return self.txt_upper_tolerance.text()
    
    @property
    def ingredient_qty_ltol(self) -> float | None:
        """Return the ingredient quantity lower tolerance."""
        return self.txt_lower_tolerance.text()

    def set_ingredient_qty(self, qty: float) -> None:
        """Set the ingredient quantity."""
        with block_signals(self.txt_ingredient_qty):
            self.txt_ingredient_qty.setText(qty)

    def set_ingredient_qty_unit(self, unit: str) -> None:
        """Set the ingredient quantity unit."""
        with block_signals(self.cmb_ingredient_qty_units):
            self.cmb_ingredient_qty_units.setCurrentText(unit)

    def set_ingredient_qty_utol(self, utol: float) -> None:
        """Set the ingredient quantity upper tolerance."""
        with block_signals(self.txt_upper_tolerance):
            self.txt_upper_tolerance.setText(utol)

    def set_ingredient_qty_ltol(self, ltol: float) -> None:
        """Set the ingredient quantity lower tolerance."""
        with block_signals(self.txt_lower_tolerance):
            self.txt_lower_tolerance.setText(ltol)

    def _build_ui(self):
        # Create a horizontal layout
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(5, 5, 5, 5)

        # Create a label and add it to the layout
        label = QLabel(self.ingredient_name)
        layout.addWidget(label)

        # Add a stretch
        layout.addStretch(1)

        # Create a textbox for the ingredient quantity
        self.txt_ingredient_qty = NumericLineEdit()
        # Set the max width of the textbox
        self.txt_ingredient_qty.setMaximumWidth(60)
        layout.addWidget(self.txt_ingredient_qty)

        # Create a dropdown for qty units
        self.cmb_ingredient_qty_units = QComboBox()
        # Add some units to the dropdown
        # These will utimately get pulled from a config
        # TODO - pull units from config
        self.cmb_ingredient_qty_units.addItems(["g", "kg", "lb"])
        layout.addWidget(self.cmb_ingredient_qty_units)

        # Create a vertical layout for tolerances
        tolerance_layout = QVBoxLayout()
        # Remove the padding
        tolerance_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(tolerance_layout)
        # Create a horizontal layout for the upper tol
        upper_tol_layout = QHBoxLayout()
        tolerance_layout.addLayout(upper_tol_layout)
        # Add a plus label
        label = QLabel("+")
        # Set the width
        label.setMaximumWidth(10)
        # Centre the text in the label
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upper_tol_layout.addWidget(label)
        # Add a textbox
        self.txt_upper_tolerance = NumericLineEdit()
        # Set the max width of the textbox
        self.txt_upper_tolerance.setMaximumWidth(30)
        upper_tol_layout.addWidget(self.txt_upper_tolerance)
        # Add a label for '%'
        label = QLabel("%")
        upper_tol_layout.addWidget(label)
        # Create a horizontal layout for the lower tol
        lower_tol_layout = QHBoxLayout()
        tolerance_layout.addLayout(lower_tol_layout)
        # Add a - label
        label = QLabel("-")
        # Set the width
        label.setMaximumWidth(10)
        # Centre the text in the label
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lower_tol_layout.addWidget(label)
        # Add a textbox
        self.txt_lower_tolerance = NumericLineEdit()
        # Set the max width of the textbox
        self.txt_lower_tolerance.setMaximumWidth(30)
        lower_tol_layout.addWidget(self.txt_lower_tolerance)
        # Add a label for '%'
        label = QLabel("%")
        lower_tol_layout.addWidget(label)
