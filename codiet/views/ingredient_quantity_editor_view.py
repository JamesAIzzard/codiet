from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QVariant

class IngredientQuantityEditorView(QWidget):
    """UI element to allow the user to edit an ingredient quantity."""

    # Define signals
    ingredientQtyChanged = pyqtSignal(QVariant)
    ingredientQtyUnitChanged = pyqtSignal(str)
    ingredientQtyUTolChanged = pyqtSignal(QVariant)
    ingredientQtyLTolChanged = pyqtSignal(QVariant)

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
        # Set any values that were passed in.
        self.ingredient_qty_value = ingredient_qty
        self.ingredient_qty_unit = ingredient_qty_unit
        self.ingredient_qty_utol = ingredient_qty_utol
        self.ingredient_qty_ltol = ingredient_qty_ltol

    @property
    def ingredient_qty_value(self) -> float | None:
        """Return the ingredient quantity."""
        return self.txt_ingredient_qty.text()
    
    @ingredient_qty_value.setter
    def ingredient_qty_value(self, value: float | None) -> None:
        """Set the ingredient quantity."""
        with block_signals(self.txt_ingredient_qty):
            self.txt_ingredient_qty.setText(value)
    
    @property
    def ingredient_qty_unit(self) -> str:
        """Return the ingredient quantity unit."""
        return self.cmb_ingredient_qty_units.currentText()
    
    @ingredient_qty_unit.setter
    def ingredient_qty_unit(self, value: str) -> None:
        """Set the ingredient quantity unit."""
        with block_signals(self.cmb_ingredient_qty_units):
            self.cmb_ingredient_qty_units.setCurrentText(value)
    
    @property
    def ingredient_qty_utol(self) -> float | None:
        """Return the ingredient quantity upper tolerance."""
        return self.txt_upper_tolerance.text()
    
    @ingredient_qty_utol.setter
    def ingredient_qty_utol(self, value: float | None) -> None:
        """Set the ingredient quantity upper tolerance."""
        with block_signals(self.txt_upper_tolerance):
            self.txt_upper_tolerance.setText(value)
    
    @property
    def ingredient_qty_ltol(self) -> float | None:
        """Return the ingredient quantity lower tolerance."""
        return self.txt_lower_tolerance.text()
    
    @ingredient_qty_ltol.setter
    def ingredient_qty_ltol(self, value: float | None) -> None:
        """Set the ingredient quantity lower tolerance."""
        with block_signals(self.txt_lower_tolerance):
            self.txt_lower_tolerance.setText(value)

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
        # Emit a signal when the text changes
        self.txt_ingredient_qty.lostFocus.connect(self.ingredientQtyChanged.emit)

        # Create a dropdown for qty units
        self.cmb_ingredient_qty_units = QComboBox()
        # Add some units to the dropdown
        # These will utimately get pulled from a config
        self.cmb_ingredient_qty_units.addItems(["g", "kg", "lb"])
        layout.addWidget(self.cmb_ingredient_qty_units)
        # Emit a signal when the text changes
        self.cmb_ingredient_qty_units.currentTextChanged.connect(self.ingredientQtyUnitChanged.emit)

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
        # Emit a signal when the text changes
        self.txt_upper_tolerance.lostFocus.connect(self.ingredientQtyUTolChanged.emit)
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
        # Emit a signal when the text changes
        self.txt_lower_tolerance.lostFocus.connect(self.ingredientQtyLTolChanged.emit)
        # Set the max width of the textbox
        self.txt_lower_tolerance.setMaximumWidth(30)
        lower_tol_layout.addWidget(self.txt_lower_tolerance)
        # Add a label for '%'
        label = QLabel("%")
        lower_tol_layout.addWidget(label)
