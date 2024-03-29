from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QComboBox,
)

from codiet.utils.pyqt import block_signals
from codiet.views.custom_line_editors import NumericLineEdit

class IngredientNutrientEditorView(QWidget):
    def __init__(self, nutrient_name: str):
        super().__init__()
        
        self.nutrient_name = nutrient_name

        # Construct the UI
        self._build_ui()

    def update_nutrient_mass(self, mass: float):
        """Updates the nutrient mass."""
        with block_signals(self.txt_nutrient_mass):
            self.txt_nutrient_mass.setText(mass)

    def update_nutrient_mass_units(self, units: str):
        """Updates the nutrient mass units."""
        with block_signals(self.cmb_mass_units):
            self.cmb_mass_units.setCurrentText(units)

    def update_ingredient_mass(self, mass: float):
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

        # Create a dropdown for mass units
        self.cmb_mass_units = QComboBox()
        # Add some mass units to the dropdown
        # These will utimately get pulled from a config
        # TODO - pull mass units from config
        self.cmb_mass_units.addItems(["g", "mg", "µg"])
        layout.addWidget(self.cmb_mass_units)

        # Create a label
        label = QLabel(" per ")
        layout.addWidget(label)

        # Create a textbox for ignredient mass
        self.txt_ingredient_mass = NumericLineEdit()
        # Set the max width of the textbox
        self.txt_ingredient_mass.setMaximumWidth(60)
        layout.addWidget(self.txt_ingredient_mass)
        
        # Create a dropdown for mass units
        self.cmb_ingredient_mass_units = QComboBox()
        # Add some mass units to the dropdown
        # These will utimately get pulled from a config
        # TODO - pull mass units from config
        self.cmb_ingredient_mass_units.addItems(["g", "kg"])
        layout.addWidget(self.cmb_ingredient_mass_units)

        # Add a little space at either end of the widget
        layout.setContentsMargins(5, 0, 5, 0)
