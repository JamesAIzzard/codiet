from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

from codiet.views.text_editors.numeric_line_editor import NumericLineEditor
from codiet.views.units.unit_dropdown import UnitDropdown

class NutrientQuantityEditorView(QWidget):
    """UI element for quantity of a nutrient in an ingredient.

    Signals:
        nutrientMassChanged(int, float): Emitted when the nutrient mass value is changed.
            The signal carries the global nutrient ID and the new mass value.
        nutrientMassUnitsChanged(int, int): Emitted when the nutrient mass unit is changed.
            The signal carries the global nutrient ID and the new unit ID.    
    """

    nutrientMassChanged = pyqtSignal(int, float)
    nutrientMassUnitsChanged = pyqtSignal(int, int)

    def __init__(
            self,
            global_nutrient_id: int,
            nutrient_name: str,
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)

        # Store the global nutrient ID and nutrient name
        self._global_nutrient_id = global_nutrient_id
        self._nutrient_name = nutrient_name

        # Build the UI
        self._build_ui()

        # Connect signals and slots
        # When the mass value textbox loses focus, emit the nutrientMassChanged signal
        self.nutrient_mass.lostFocus.connect(
            lambda value: self.nutrientMassChanged.emit(self._global_nutrient_id, value)
        )
        # When the mass units dropdown changes, emit the nutrientMassUnitsChanged signal
        self.nutrient_mass_units.unitChanged.connect(self.nutrientMassUnitsChanged.emit)       

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
        self.nutrient_mass = NumericLineEditor()
        # Limit the textbox to 10 pixels
        self.nutrient_mass.setMaximumWidth(60)
        layout.addWidget(self.nutrient_mass)

        # Create a dropdown for mass units
        self.nutrient_mass_units = UnitDropdown()
        layout.addWidget(self.nutrient_mass_units)

        # Add a little space at either end of the widget
        layout.setContentsMargins(5, 0, 5, 0)