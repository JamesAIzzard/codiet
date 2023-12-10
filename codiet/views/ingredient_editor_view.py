from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox
from PyQt6.QtGui import QFont

from codiet.views.ingredient_name_editor_view import IngredientNameEditorView
from codiet.views.ingredient_cost_editor_view import IngredientCostEditorView
from codiet.views.ingredient_density_editor_view import IngredientDensityEditorView
from codiet.views.ingredient_pc_mass_editor_view import IngredientPcMassEditorView
from codiet.views.ingredient_flag_editor_view import IngredientFlagEditorView
from codiet.views.ingredient_gi_editor_view import IngredientGIEditorView

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

        # Create a vertical layout for the first column
        column1_layout = QVBoxLayout()

        # Create the basic info group
        basic_info_group = QGroupBox("Basic Info")
        basic_info_group_layout = QVBoxLayout()

        # Create an instance of IngredientNameWidget and add it to a vertical layout
        self.ingredientNameWidget = IngredientNameEditorView()
        basic_info_group_layout.addWidget(self.ingredientNameWidget)

        # Create an instance of IngredientCostWidget and add it to a vertical layout
        self.ingredientCostWidget = IngredientCostEditorView()
        basic_info_group_layout.addWidget(self.ingredientCostWidget)

        # Set the layout for the basic info group
        basic_info_group.setLayout(basic_info_group_layout)

        # Add the basic info group to the column1 layout
        column1_layout.addWidget(basic_info_group)

        # Create the Bulk Properties group
        bulk_properties_group = QGroupBox("Bulk Properties")
        bulk_properties_group_layout = QVBoxLayout()

        # Create an instance of the density widget and add it to a vertical layout
        self.ingredientDensityWidget = IngredientDensityEditorView()
        bulk_properties_group_layout.addWidget(self.ingredientDensityWidget)

        # Create an instance of the piece mass widget and add it to a vertical layout
        self.ingredientPcMassWidget = IngredientPcMassEditorView()
        bulk_properties_group_layout.addWidget(self.ingredientPcMassWidget)

        # Set the layout for the bulk properties group
        bulk_properties_group.setLayout(bulk_properties_group_layout)

        # Add the bulk properties group to the column1 layout
        column1_layout.addWidget(bulk_properties_group)

        # Add the flags widget to the column1 layout
        self.ingredientFlagWidget = IngredientFlagEditorView()
        column1_layout.addWidget(self.ingredientFlagWidget)

        # Add the GI widget to the column1 layout
        self.ingredientGIWidget = IngredientGIEditorView()
        column1_layout.addWidget(self.ingredientGIWidget)

        # Add stretch to end of layout
        column1_layout.addStretch(1)

        # Add the column1 layout to the columns layout
        columns_layout.addLayout(column1_layout, 1)

        # Create a placeholder widget for the second column and add it to a vertical layout
        placeholder = QWidget()
        column2_layout = QVBoxLayout()
        column2_layout.addWidget(placeholder)
        column2_layout.addStretch(1)  # Add a stretch to the end of the layout
        columns_layout.addLayout(column2_layout, 1)

        # Add the columns layout to the page layout
        page_layout.addLayout(columns_layout)

        # Set the layout for the page
        self.setLayout(page_layout)