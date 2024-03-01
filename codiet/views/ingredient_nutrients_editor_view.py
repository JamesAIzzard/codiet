from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QCheckBox,
    QLineEdit,
    QPushButton
)

from codiet.views.ingredient_nutrient_editor_view import IngredientNutrientEditorView

class IngredientNutrientsEditorView(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

        # Create a dict to store widgets by nutrient name
        self.nutrient_widgets = {}

    def _init_ui(self):
        """Initializes the UI elements."""
        # Create vertical layout as the top level
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Reduce the vertical padding in this layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Put a group inside this layout
        group_box = QGroupBox("Nutrients")
        layout.addWidget(group_box)

        # Put a vertical layout inside the group box
        lyt_top_level = QVBoxLayout()
        group_box.setLayout(lyt_top_level)

        # Add an HBox layout for 'Hide Complete' control
        lyt_hide_complete = QHBoxLayout()
        lyt_top_level.addLayout(lyt_hide_complete)

        # Add a checkbox to 'Hide Completed'
        self.chk_hide_completed = QCheckBox("Hide Completed")
        lyt_hide_complete.addWidget(self.chk_hide_completed)
        # Add the label
        self.lbl_hide_completed = QLabel("Hide Completed")

        # Add an HBox layout for the filter controls
        lyt_filter = QHBoxLayout()
        lyt_top_level.addLayout(lyt_filter)
        # Add the label
        self.lbl_filter = QLabel("Filter: ")
        lyt_filter.addWidget(self.lbl_filter)
        # Add the filter input
        self.txt_filter = QLineEdit()
        lyt_filter.addWidget(self.txt_filter)
        # Add the clear button
        self.btn_clear_filter = QPushButton("X")
        # Set width
        self.btn_clear_filter.setMaximumWidth(20)
        lyt_filter.addWidget(self.btn_clear_filter)

        # Create a listbox for the nutrient rows
        self.listWidget = QListWidget()
        lyt_top_level.addWidget(self.listWidget)

    def add_nutrient(self, nutrient_name: str):
        """Adds a new nutrient row to the list widget."""
        # Add a new row to the list
        listItem = QListWidgetItem(self.listWidget)
        nutrient_widget = IngredientNutrientEditorView(nutrient_name)
        listItem.setSizeHint(nutrient_widget.sizeHint())
        self.listWidget.addItem(listItem)
        self.listWidget.setItemWidget(listItem, nutrient_widget)
        # Store the widget
        self.nutrient_widgets[nutrient_name] = nutrient_widget

    def hide_nutrient(self, nutrient_name: str):
        """Hides a nutrient row in the list widget."""
        self.nutrient_widgets[nutrient_name].hide()

    def show_nutrient(self, nutrient_name: str):
        """Shows a nutrient row in the list widget."""
        self.nutrient_widgets[nutrient_name].show()

    def show_all_nutrients(self):
        """Shows all nutrient rows in the list widget."""
        for nutrient_widget in self.nutrient_widgets.values():
            nutrient_widget.show()