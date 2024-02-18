from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PyQt6.QtGui import QFont

from codiet.views.ingredient_basic_info_editor_view import IngredientBasicInfoEditorView
from codiet.views.ingredient_bulk_properties_editor_view import IngredientBulkPropertiesEditorView
from codiet.views.flag_editor_view import FlagEditorView
from codiet.views.gi_editor_view import GIEditorView
from codiet.views.ingredient_nutrients_editor_view import IngredientNutrientsEditorView


class IngredientEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a vertical layout for the page
        page_layout = QVBoxLayout()

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

        # Create the Basic Info widget
        self.ingredient_basic_info_editor_view = IngredientBasicInfoEditorView()
        column1_layout.addWidget(self.ingredient_basic_info_editor_view)

        # Create the bulk properties widget
        self.ingredient_bulk_properties_editor_view = IngredientBulkPropertiesEditorView()
        column1_layout.addWidget(self.ingredient_bulk_properties_editor_view)

        # Add the flags widget to the column1 layout
        self.flag_editor_view = FlagEditorView()
        column1_layout.addWidget(self.flag_editor_view)

        # Add the GI widget to the column1 layout
        self.ingredient_gi_editor_view = GIEditorView()
        column1_layout.addWidget(self.ingredient_gi_editor_view)

        # Add stretch to end of layout
        column1_layout.addStretch(1)


        # Create the second column.
        column2_layout = QVBoxLayout()
        columns_layout.addLayout(column2_layout, 1)

        # Create a nutrient editor widget and add it to the column2 layout
        self.nutrient_editor_view = IngredientNutrientsEditorView()
        column2_layout.addWidget(self.nutrient_editor_view)

        # Add a save ingredient button to the bottom of the page
        self.save_ingredient_button = QPushButton("Save Ingredient")
        # Limit the width of the button
        self.save_ingredient_button.setMaximumWidth(150)
        page_layout.addWidget(self.save_ingredient_button)

        # Set the layout for the page
        self.setLayout(page_layout)
