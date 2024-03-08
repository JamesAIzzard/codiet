from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QLineEdit,
    QTextEdit,
    QComboBox
)
from PyQt6.QtGui import QFont

from codiet.views.flag_editor_view import FlagEditorView
from codiet.views.gi_editor_view import GIEditorView
from codiet.views.ingredient_nutrients_editor_view import IngredientNutrientsEditorView


class IngredientEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Build the UI
        self._build_ui()

    def _build_ui(self):
        """Build the UI for the ingredient editor page."""
        # Create a vertical layout for the page
        page_layout = QVBoxLayout()
        # Set the layout for the page
        self.setLayout(page_layout)


        # Create a label and add it to the page layout
        label = QLabel("Ingredient Editor")
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        page_layout.addWidget(label)

        # Create a horizontal layout for the columns
        columns_layout = QHBoxLayout()
        page_layout.addLayout(columns_layout)

        # Create a vertical layout for the first column
        column1_layout = QVBoxLayout()
        columns_layout.addLayout(column1_layout, 1)

        # Add the basic info section to the column 1 layout
        self._build_basic_info_UI(column1_layout)

        # Add the cost editor to the column 1 layout
        self._build_cost_UI(column1_layout)

        # Add the bulk properties widget to the column1 layout
        self._build_bulk_properties_UI(column1_layout)

        # Add the flags widget to the column1 layout
        self.flag_editor_view = FlagEditorView()
        column1_layout.addWidget(self.flag_editor_view)

        # Add the GI widget to the column1 layout
        self.ingredient_gi_editor_view = GIEditorView()
        column1_layout.addWidget(self.ingredient_gi_editor_view)

        # Add stretch to end of layout
        column1_layout.addStretch(1)

        # Create the second column.
        lyt_col_2 = QVBoxLayout()
        columns_layout.addLayout(lyt_col_2, 1)

        # Create a nutrient editor widget and add it to the column2 layout
        self.nutrient_editor_view = IngredientNutrientsEditorView()
        lyt_col_2.addWidget(self.nutrient_editor_view)

        # Add a save ingredient button to the bottom of the page
        self.btn_save_ingredient = QPushButton("Save Ingredient")
        # Limit the width of the button
        self.btn_save_ingredient.setMaximumWidth(150)
        page_layout.addWidget(self.btn_save_ingredient)

    def _build_basic_info_UI(self, container: QVBoxLayout):
        """Build the UI for the basic info section of the ingredient editor page."""

        # Create the basic info groupbox
        gb_basic_info = QGroupBox("Basic Info")
        container.addWidget(gb_basic_info)

        # Put a vertical layout inside the basic info groubox
        lyt_top_level = QVBoxLayout()
        gb_basic_info.setLayout(lyt_top_level)

        # Create a horizontal layout for name and textbox
        lyt_ingredient_name = QHBoxLayout()
        lyt_top_level.addLayout(lyt_ingredient_name)

        # Create a label and add it to the layout
        label = QLabel("Name:")
        lyt_ingredient_name.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_ingredient_name = QLineEdit()
        lyt_ingredient_name.addWidget(self.txt_ingredient_name)

        # Reduce the vertical padding in this layout
        lyt_ingredient_name.setContentsMargins(0, 0, 0, 0)

        # Add a description field and multiline textbox
        label = QLabel("Description:")
        lyt_top_level.addWidget(label)
        self.txt_ingredient_description = QTextEdit()
        lyt_top_level.addWidget(self.txt_ingredient_description)

    def _build_cost_UI(self, container: QVBoxLayout):
        """Build the UI for the cost section of the ingredient editor page."""
        
        # Create the cost groupbox
        gb_cost = QGroupBox("Cost")
        container.addWidget(gb_cost)

        # Create a horizontal layout for the cost section
        lyt_cost = QHBoxLayout()
        gb_cost.setLayout(lyt_cost)

        # Create the first label
        label = QLabel("Cost: £")
        lyt_cost.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_cost = QLineEdit()
        lyt_cost.addWidget(self.txt_cost)

        # Create a second label
        label = QLabel(" per ")
        lyt_cost.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_cost_quantity = QLineEdit()
        lyt_cost.addWidget(self.txt_cost_quantity)

        # Create a units dropdown
        self.cmb_cost_unit = QComboBox()
        # Temporarily add units, these will get pulled from config file later
        # TODO - pull units from config file
        self.cmb_cost_unit.addItems(["g", "kg", "ml", "l"])
        lyt_cost.addWidget(self.cmb_cost_unit)   

    def _build_bulk_properties_UI(self, container: QVBoxLayout):
        """Build the UI for the bulk properties section of the ingredient editor page."""
        # Create the bulk properties groupbox
        gb_bulk_properties = QGroupBox("Bulk Properties")
        container.addWidget(gb_bulk_properties)

        # Add a vertical layout inside the groubox
        lyt_top_level = QVBoxLayout()
        gb_bulk_properties.setLayout(lyt_top_level)

        # Add a horizontal layout for the density editor
        lyt_density = QHBoxLayout()
        lyt_top_level.addLayout(lyt_density)

        # Create a label and add it to the layout
        label = QLabel("Density:")
        lyt_density.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_density = QLineEdit()
        lyt_density.addWidget(self.txt_density)

        # Create a volume units dropdown and add it to the layout
        self.cmb_vol_units = QComboBox()
        # Temporarily add units, these will get pulled from config file later
        # TODO - pull units from config file
        self.cmb_vol_units.addItems(["ml", "l"])
        lyt_density.addWidget(self.cmb_vol_units)

        # Create another label and add it to the layout
        label = QLabel(" weighs ")
        lyt_density.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_mass = QLineEdit()
        lyt_density.addWidget(self.txt_mass)

        # Create a mass units dropdown and add it to the layout
        self.cmb_mass_units = QComboBox()
        # Temporarily add units, these will get pulled from config file later
        # TODO - pull units from config file
        self.cmb_mass_units.addItems(["g", "kg"])
        lyt_density.addWidget(self.cmb_mass_units)
        
        # Add a horizontal layout for the piece mass editor
        lyt_piece_mass = QHBoxLayout()
        lyt_top_level.addLayout(lyt_piece_mass)

        # Create a label and add it to the layout
        label = QLabel("Piece Mass:")
        lyt_piece_mass.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_piece_qty = QLineEdit()
        lyt_piece_mass.addWidget(self.txt_piece_qty)

        # Create another label
        label = QLabel(" piece(s) weighs ")
        lyt_piece_mass.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_piece_mass = QLineEdit()
        lyt_piece_mass.addWidget(self.txt_piece_mass)

        # Create a mass units dropdown and add it to the layout
        self.cmb_mass_units = QComboBox()
        # Temporarily add units, these will get pulled from config file later
        # TODO - pull units from config file
        self.cmb_mass_units.addItems(["g", "kg"])
        lyt_piece_mass.addWidget(self.cmb_mass_units)

# EOF