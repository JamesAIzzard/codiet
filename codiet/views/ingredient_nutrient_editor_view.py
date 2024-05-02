from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QComboBox,
)
from PyQt6.QtCore import pyqtSignal

from codiet.utils.pyqt import block_signals
from codiet.views.custom_line_editors import NumericLineEdit


class IngredientNutrientEditorView(QWidget):
    """UI element for quantity of a nutrient in an ingredient."""

    # Define signals
    nutrientMassChanged = pyqtSignal(str, float)
    nutrientMassCleared = pyqtSignal(str)
    nutrientMassUnitsChanged = pyqtSignal(str, str)
    ingredientMassChanged = pyqtSignal(str, float)
    ingredientMassCleared = pyqtSignal(str)
    ingredientMassUnitsChanged = pyqtSignal(str, str)

    def __init__(self, nutrient_name: str):
        super().__init__()

        self.nutrient_name = nutrient_name

        # Construct the UI
        self._build_ui()

    @property
    def nutrient_mass(self) -> float | None:
        """Returns the nutrient mass."""
        return self.txt_nutrient_mass.text()

    @property
    def nutrient_mass_units(self) -> str:
        """Returns the nutrient mass units."""
        return self.cmb_mass_units.currentText()

    @property
    def ingredient_mass(self) -> float | None:
        """Returns the ingredient mass."""
        return self.txt_ingredient_mass.text()

    @property
    def ingredient_mass_units(self) -> str:
        """Returns the ingredient mass units."""
        return self.cmb_ingredient_mass_units.currentText()

    def update_nutrient_mass(self, mass: float | None):
        """Updates the nutrient mass."""
        with block_signals(self.txt_nutrient_mass):
            self.txt_nutrient_mass.setText(mass)

    def update_nutrient_mass_units(self, units: str):
        """Updates the nutrient mass units."""
        with block_signals(self.cmb_mass_units):
            self.cmb_mass_units.setCurrentText(units)

    def update_ingredient_mass(self, mass: float | None):
        """Updates the ingredient mass."""
        with block_signals(self.txt_ingredient_mass):
            self.txt_ingredient_mass.setText(mass)

    def update_ingredient_mass_units(self, units: str):
        """Updates the ingredient mass units."""
        with block_signals(self.cmb_ingredient_mass_units):
            self.cmb_ingredient_mass_units.setCurrentText(units)

    def _build_ui(self):
        """Initializes the UI elements."""
        # Create a horizontal layout for the widget
        layout = QHBoxLayout()
        self.setLayout(layout)
        # Reduce the horizontal padding in this layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a label and add it to the layout
        label = QLabel(self.nutrient_name + ":")
        layout.addWidget(label)

        # Add a stretch
        layout.addStretch(1)

        # Create a textbox for nutrient mass
        self.txt_nutrient_mass = NumericLineEdit()
        # Limit the textbox to 10 chars
        self.txt_nutrient_mass.setMaximumWidth(60)
        layout.addWidget(self.txt_nutrient_mass)
        # Connect the valueChanged signal to the nutrientMassChanged signal
        self.txt_nutrient_mass.valueChanged.connect(
            lambda value: self.nutrientMassChanged.emit(self.nutrient_name, value)
        )
        # Connect the valueCleared signal to the nutrientMassCleared signal
        self.txt_nutrient_mass.valueCleared.connect(
            lambda: self.nutrientMassCleared.emit(self.nutrient_name)
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
            lambda units: self.nutrientMassUnitsChanged.emit(self.nutrient_name, units)
        )

        # Create a label
        label = QLabel(" per ")
        layout.addWidget(label)

        # Create a textbox for ignredient mass
        self.txt_ingredient_mass = NumericLineEdit()
        # Set the max width of the textbox
        self.txt_ingredient_mass.setMaximumWidth(60)
        layout.addWidget(self.txt_ingredient_mass)
        # Connect the valueChanged signal to the ingredientMassChanged signal
        self.txt_ingredient_mass.valueChanged.connect(
            lambda value: self.ingredientMassChanged.emit(self.nutrient_name, value)
        )
        # Connect the valueCleared signal to the ingredientMassCleared signal
        self.txt_ingredient_mass.valueCleared.connect(
            lambda: self.ingredientMassCleared.emit(self.nutrient_name)
        )

        # Create a dropdown for mass units
        self.cmb_ingredient_mass_units = QComboBox()
        # Add some mass units to the dropdown
        # These will utimately get pulled from a config
        # TODO - pull mass units from config
        self.cmb_ingredient_mass_units.addItems(["g", "kg"])
        layout.addWidget(self.cmb_ingredient_mass_units)
        # Connect the currentTextChanged signal to the ingredientMassUnitsChanged signal
        self.cmb_ingredient_mass_units.currentTextChanged.connect(
            lambda units: self.ingredientMassUnitsChanged.emit(self.nutrient_name, units)
        )

        # Add a little space at either end of the widget
        layout.setContentsMargins(5, 0, 5, 0)
