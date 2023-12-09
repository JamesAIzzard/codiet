from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox
from PyQt6.QtGui import QFont

from codiet.views.ingredient_name_editor_view import IngredientNameEditorView
from codiet.views.ingredient_cost_editor_view import IngredientCostEditorView

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