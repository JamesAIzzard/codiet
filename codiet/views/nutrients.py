from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox
)
from PyQt6.QtCore import pyqtSignal, QVariant

from codiet.utils.pyqt import block_signals
from codiet.views.text_editors import NumericLineEdit
from codiet.views.search import SearchColumnView

class NutrientQuantitiesEditorView(QWidget):
    """UI element for editing the quantities of nutrients in an ingredient."""
    nutrientQuantityChanged = pyqtSignal(str, QVariant, str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build_ui(*args, **kwargs)

    def _build_ui(self):
        """Build the UI elements."""
        # Create a vertical layout
        lyt_top_level = QVBoxLayout()
        self.setLayout(lyt_top_level)
        # Add a horizontal layout to hold the ingredient reference qty
        lyt_ingredient_ref_qty = QHBoxLayout()
        lyt_top_level.addLayout(lyt_ingredient_ref_qty)
        # Add the ingredient reference qty label
        lbl_ingredient_ref_qty = QLabel("Ingredient Reference Quantity:")
        lyt_ingredient_ref_qty.addWidget(lbl_ingredient_ref_qty)
        # Add the ingredient reference qty editor
        self.txt_ingredient_ref_qty = NumericLineEdit()
        lyt_ingredient_ref_qty.addWidget(self.txt_ingredient_ref_qty)
        # Preload the textbox as 100
        self.txt_ingredient_ref_qty.setText(100)
        # Add the ingredient reference qty units combobox
        self.cmb_ingredient_ref_qty_units = QComboBox()
        lyt_ingredient_ref_qty.addWidget(self.cmb_ingredient_ref_qty_units)
        # Add some units
        self.cmb_ingredient_ref_qty_units.addItems(["g", "kg", "mg", "ug", "ml", "l", "tsp", "tbsp", "cup", "fl oz", "pt", "qt", "gal"])
        # Add a stretch
        lyt_ingredient_ref_qty.addStretch(1)
        # Add the search column
        self.search_column = SearchColumnView()
        lyt_top_level.addWidget(self.search_column)

class NutrientQuantityEditorView(QWidget):
    """UI element for quantity of a nutrient in an ingredient."""

    # Define signals
    nutrientMassChanged = pyqtSignal(str, QVariant)
    nutrientMassUnitsChanged = pyqtSignal(str, str)

    def __init__(self, nutrient_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._nutrient_name = nutrient_name
        self._build_ui()

    @property
    def nutrient_mass(self) -> float | None:
        """Returns the nutrient mass."""
        return self.txt_nutrient_mass.text()

    @property
    def nutrient_mass_units(self) -> str:
        """Returns the nutrient mass units."""
        return self.cmb_mass_units.currentText()

    def update_nutrient_mass(self, mass: float | None):
        """Updates the nutrient mass."""
        with block_signals(self.txt_nutrient_mass):
            self.txt_nutrient_mass.setText(mass)

    def update_nutrient_mass_units(self, units: str):
        """Updates the nutrient mass units."""
        with block_signals(self.cmb_mass_units):
            self.cmb_mass_units.setCurrentText(units)

    def _build_ui(self):
        """Initializes the UI elements."""
        # Create a horizontal layout for the widget
        layout = QHBoxLayout()
        self.setLayout(layout)
        # Reduce the horizontal padding in this layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a label and add it to the layout
        label = QLabel(self._nutrient_name + ":")
        layout.addWidget(label)

        # Add a stretch
        layout.addStretch(1)

        # Create a textbox for nutrient mass
        self.txt_nutrient_mass = NumericLineEdit()
        # Limit the textbox to 10 pixels
        self.txt_nutrient_mass.setMaximumWidth(60)
        layout.addWidget(self.txt_nutrient_mass)
        # Connect the valueChanged signal to the nutrientMassChanged signal
        self.txt_nutrient_mass.lostFocus.connect(
            lambda value: self.nutrientMassChanged.emit(self._nutrient_name, value)
        )

        # Create a dropdown for mass units
        self.cmb_mass_units = QComboBox()
        # Add some mass units to the dropdown
        # These will utimately get pulled from a config
        # TODO - pull mass units from config
        self.cmb_mass_units.addItems(["g", "mg", "ug"])
        layout.addWidget(self.cmb_mass_units)
        # Connect the currentTextChanged signal to the nutrientMassUnitsChanged signal
        self.cmb_mass_units.currentTextChanged.connect(
            lambda units: self.nutrientMassUnitsChanged.emit(self._nutrient_name, units)
        )

        # Add a little space at either end of the widget
        layout.setContentsMargins(5, 0, 5, 0)