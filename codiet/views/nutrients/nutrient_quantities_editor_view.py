from PyQt6.QtCore import pyqtSignal, QVariant
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox

from codiet.views.text_editors.numeric_line_editor import NumericLineEditor
from codiet.views.search.search_column_view import SearchColumnView

class NutrientQuantitiesEditorView(QWidget):
    """UI element for editing the quantities of nutrients in an ingredient.
    Signals:
        nutrientQuantityAdded(int, int): Emitted when a nutrient is added to the ingredient.
            The signal carries the global nutrient ID and the nutrient mass ID.
        nutrientQuantityChanged(int, QVariant, str): Emitted when the quantity of a nutrient is changed.
            The signal carries the global nutrient ID, the nutrient mass, and the nutrient mass ID.
        nutrientQuantityRemoved(int): Emitted when a nutrient is removed from the ingredient.
            The signal carries the global nutrient ID.
    """
    nutrientQuantityAdded = pyqtSignal(int, int)
    nutrientQuantityChanged = pyqtSignal(int, QVariant, int)
    nutrientQuantityRemoved = pyqtSignal(int)

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
        self.txt_ingredient_ref_qty = NumericLineEditor()
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
        # Add the display column
        self.display_column = SearchColumnView()
        lyt_top_level.addWidget(self.display_column)
