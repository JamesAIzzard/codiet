from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QGroupBox,
    QTextEdit,
)
from PyQt6.QtGui import QFont

from codiet.views.nutrient_targets_editor_view import NutrientTargetsEditorView
from codiet.views.flag_editor_view import FlagEditorView
from codiet.views.custom_line_editors import NumericLineEdit

class MealGoalDefaultsEditorView(QWidget):
    """The UI element to allow the user to edit the default values applied
    to a new meal goal."""
    def __init__(self):
        super().__init__()

        # Build the UI
        self._build_ui()


    def _build_ui(self):
        """Build the UI for the meal goal defaults editor page."""
        # Create a vertical layout for the page
        page_layout = QVBoxLayout()
        self.setLayout(page_layout)

        # Create a label and add it to the layout
        label = QLabel("Meal Goal Default Values Editor")
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        page_layout.addWidget(label)

        # Create a horizontal layout for the columns
        columns_layout = QHBoxLayout()
        page_layout.addLayout(columns_layout)

        # Create the first column
        column1_layout = QVBoxLayout()
        columns_layout.addLayout(column1_layout)

        # Add a flag editor view
        self.flag_editor_view = FlagEditorView()
        column1_layout.addWidget(self.flag_editor_view)

        # Add the GI widget to the column1 layout
        self._build_gi_UI(column1_layout)

        # Create a second column
        column2_layout = QVBoxLayout()
        columns_layout.addLayout(column2_layout)

        # Put a nutrient targets editor view in it
        self.nutrient_targets_editor_view = NutrientTargetsEditorView()
        column2_layout.addWidget(self.nutrient_targets_editor_view)

        # At the bottom of the page, put a save meal button
        self.btn_save_meal = QPushButton("Save Meal")
        self.btn_save_meal.setMaximumWidth(150)
        page_layout.addWidget(self.btn_save_meal)
        
    def _build_gi_UI(self, container: QVBoxLayout):
        """Build the UI for the GI section of the ingredient editor page."""
        # Create the GI groupbox
        gb_gi = QGroupBox("GI")
        container.addWidget(gb_gi)

        # Put a horizontal layout inside the group box
        column_layout = QHBoxLayout()
        gb_gi.setLayout(column_layout)

        # Create a label and add it to the layout
        label = QLabel("Glycemic Index (Carbohydrate Only):")
        column_layout.addWidget(label)

        # Create a line edit and add it to the layout
        self.txt_gi = NumericLineEdit()
        column_layout.addWidget(self.txt_gi)
