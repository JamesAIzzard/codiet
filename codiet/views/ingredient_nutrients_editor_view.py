from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QListWidget,
    QListWidgetItem,
)
from PyQt6.QtCore import pyqtSignal, QVariant

from codiet.models.ingredients import IngredientNutrientQuantity
from codiet.views.search_views import SearchTermView
from codiet.views.ingredient_nutrient_editor_view import IngredientNutrientEditorView


class IngredientNutrientsEditorView(QWidget):
    """The UI element to allow the user to edit the nutrients of an ingredient."""
    
    # Define signals
    nutrientFilterChanged = pyqtSignal(str)
    nutrientFilterCleared = pyqtSignal()
    nutrientMassChanged = pyqtSignal(str, QVariant)
    nutrientMassUnitsChanged = pyqtSignal(str, str)
    ingredientQtyChanged = pyqtSignal(str, QVariant)
    ingredientQtyUnitsChanged = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        # Construct the UI
        self._build_ui()

        # Create a dict to store widgets by nutrient name
        self.nutrient_widgets: dict[str, IngredientNutrientEditorView] = {}

    def add_nutrient(self, nutrient_name: str) -> None:
        """Adds a new nutrient row to the list widget.
        Use the controller method to also connect signals.
        """
        # If the nutrient is in the list already, raise an exception
        if nutrient_name in self.nutrient_widgets:
            raise ValueError(f"Nutrient '{nutrient_name}' is already in the list.")
        # Add a new row to the list
        listItem = QListWidgetItem(self.listWidget)
        nutrient_widget = IngredientNutrientEditorView(nutrient_name)
        # Connect signals
        nutrient_widget.nutrientMassChanged.connect(
            lambda ntr_name, qty: self.nutrientMassChanged.emit(ntr_name, qty)
        )
        nutrient_widget.nutrientMassUnitsChanged.connect(
            lambda ntr_name, units: self.nutrientMassUnitsChanged.emit(ntr_name, units)
        )
        nutrient_widget.ingredientMassChanged.connect(
            lambda ntr_name, qty: self.ingredientQtyChanged.emit(ntr_name, qty)
        )
        nutrient_widget.ingredientMassUnitsChanged.connect(
            lambda ntr_name, units: self.ingredientQtyUnitsChanged.emit(ntr_name, units)
        )
        # Set the size hint
        listItem.setSizeHint(nutrient_widget.sizeHint())
        # Add the widget to the list
        self.listWidget.addItem(listItem)
        # Set the widget for the item
        self.listWidget.setItemWidget(listItem, nutrient_widget)
        # Store the widget
        self.nutrient_widgets[nutrient_name] = nutrient_widget

    def add_nutrients(self, nutrient_names: list[str]) -> None:
        """Adds multiple nutrient rows to the list widget.
        Use update_nutrient to set the values.
        """
        for nutrient_name in nutrient_names:
            # Add the widget
            self.add_nutrient(nutrient_name)

    def update_nutrient(self, nutrient_name: str, nutrient: IngredientNutrientQuantity) -> None:
        """Updates the values of a nutrient row in the list widget."""
        # This will raise a KeyError if the nutrient is not in the list
        self.nutrient_widgets[nutrient_name].update_nutrient_mass(nutrient.nutrient_mass)
        self.nutrient_widgets[nutrient_name].update_nutrient_mass_units(nutrient.nutrient_mass_unit)
        self.nutrient_widgets[nutrient_name].update_ingredient_mass(nutrient.ingredient_quantity)
        self.nutrient_widgets[nutrient_name].update_ingredient_mass_units(nutrient.ingredient_quantity_unit)

    def update_nutrients(self, nutrients: dict[str, IngredientNutrientQuantity]):
        """Updates the values of all nutrient rows in the list widget."""
        for nutrient_name, nutrient in nutrients.items():
            self.update_nutrient(nutrient_name, nutrient)

    def remove_nutrient(self, nutrient_name: str) -> None:
        """Removes a nutrient row from the list widget."""
        # Pop the widget from the dict
        nutrient_widget = self.nutrient_widgets.pop(nutrient_name)
        # Remove the widget from the list
        self.listWidget.takeItem(self.listWidget.row(nutrient_widget)) # type: ignore

    def remove_all_nutrients(self):
        """Removes all nutrient rows from the list widget."""
        self.listWidget.clear()
        self.nutrient_widgets.clear()

    def _build_ui(self):
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

        # Add an HBox layout for the filter controls
        lyt_filter = QHBoxLayout()
        lyt_top_level.addLayout(lyt_filter)
        # Add the label
        self.lbl_filter = QLabel("Filter: ")
        lyt_filter.addWidget(self.lbl_filter)
        # Add the filter input
        self.search_term_widget = SearchTermView()
        lyt_filter.addWidget(self.search_term_widget)
        # Connect the signals
        self.search_term_widget.cancelClicked.connect(self.nutrientFilterCleared.emit)
        self.search_term_widget.searchTermChanged.connect(self.nutrientFilterChanged.emit)

        # Create a listbox for the nutrient rows
        self.listWidget = QListWidget()
        lyt_top_level.addWidget(self.listWidget)