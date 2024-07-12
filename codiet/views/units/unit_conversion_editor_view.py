from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget
from PyQt6.QtCore import pyqtSignal, QVariant

from codiet.views import block_signals
from codiet.views.text_editors.numeric_line_editor import NumericLineEdit

class UnitConversionEditorView(QWidget):
    """A widget for editing a unit conversion.
    Signals:
        conversionUpdated: Emitted when the conversion is updated.
            int: The global ID of the unit conversion.
            QVariant: The new from unit quantity, can be float or None.
            QVariant: The new to unit quantity, can be float or None.
    """

    conversionUpdated = pyqtSignal(int, QVariant, QVariant)

    def __init__(
        self,
        id: int,
        from_unit_id: int,
        to_unit_id: int,
        from_unit_display_name: str,
        to_unit_display_name: str,
        *args,
        **kwargs
    ):
        """Initialise the unit conversion editor view.
        Args:
            id (int): The global ID of the unit conversion.
            from_unit_id (int): The global ID of the from unit.
            to_unit_id (int): The global ID of the to unit.
            from_unit_display_name (str): The display name of the from unit.
            to_unit_display_name (str): The display name of the to unit.
        """
        super().__init__(*args, **kwargs)
        self.id = id
        self.from_unit_id = from_unit_id
        self.to_unit_id = to_unit_id
        self.from_unit_display_name = from_unit_display_name
        self.to_unit_display_name = to_unit_display_name
        self._build_ui()
        self.txt_from_unit_qty.textChanged.connect(self._on_conversion_updated)
        self.txt_to_unit_qty.textChanged.connect(self._on_conversion_updated)

    @property
    def from_unit_qty(self) -> float | None:
        """Return the from unit quantity.
        Returns:
            float | None: The quantity of the from unit.
        """
        return self.txt_from_unit_qty.text()
    
    @from_unit_qty.setter
    def from_unit_qty(self, value: float | None) -> None:
        """Set the from unit quantity.
        Args:
            value (float | None): The quantity of the from unit.
        Returns:
            None
        """
        with block_signals(self.txt_from_unit_qty):
            self.txt_from_unit_qty.setText(value)

    @property
    def to_unit_qty(self) -> float | None:
        """Return the to unit quantity.
        Returns:
            float | None: The quantity of the to unit.
        """
        return self.txt_to_unit_qty.text()
    
    @to_unit_qty.setter
    def to_unit_qty(self, value: float | None) -> None:
        """Set the to unit quantity.
        Args:
            value (float | None): The quantity of the to unit.
        Returns:
            None
        """
        with block_signals(self.txt_to_unit_qty):
            self.txt_to_unit_qty.setText(value)

    def flip_conversion(self) -> None:
        """Flip the conversion."""
        # Save the original quantities
        orig_lbl_from_unit = self.lbl_from_unit.text()
        orig_lbl_to_unit = self.lbl_to_unit.text()
        orig_from_unit_qty = self.from_unit_qty
        orig_to_unit_qty = self.to_unit_qty
        # Flip everything
        self.lbl_from_unit.setText(orig_lbl_to_unit)
        self.lbl_to_unit.setText(orig_lbl_from_unit)
        self.from_unit_qty = orig_to_unit_qty
        self.to_unit_qty = orig_from_unit_qty

    def _on_conversion_updated(self):
        """Called when the conversion is updated."""
        self.conversionUpdated.emit(
            self.id,
            self.from_unit_qty,
            self.to_unit_qty,
        )

    def _build_ui(self):
        """Constructs the user interface."""
        # Create a horizontal layout
        layout = QHBoxLayout()
        self.setLayout(layout)
        # Create a numeric box for the from unit quantity
        self.txt_from_unit_qty = NumericLineEdit()
        layout.addWidget(self.txt_from_unit_qty)
        # Create a label for the from unit
        self.lbl_from_unit = QLabel(self.from_unit_display_name)
        # Create a label for the equals sign
        lbl_equals = QLabel(" = ")
        layout.addWidget(lbl_equals)
        # Create a numeric box for the to unit quantity
        self.txt_to_unit_qty = NumericLineEdit()
        layout.addWidget(self.txt_to_unit_qty)
        # Create a label for the to unit
        self.lbl_to_unit = QLabel(self.to_unit_display_name)
        # Add a spacer to push the combo box to the LHS
        layout.addStretch()
