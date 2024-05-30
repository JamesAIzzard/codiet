from typing import Callable

from PyQt6.QtWidgets import QListWidgetItem

from codiet.models.nutrients import IngredientNutrientQuantity
from codiet.views.nutrients import (
    NutrientQuantitiesEditorView,
    NutrientQuantityEditorView,
)
from codiet.controllers.search import SearchColumnCtrl


class NutrientQuantitiesEditorCtrl:
    def __init__(
        self,
        view: NutrientQuantitiesEditorView,
        get_nutrient_data: Callable[[], dict[str, IngredientNutrientQuantity]],
        on_nutrient_qty_changed: Callable[[IngredientNutrientQuantity], None],
    ) -> None:
        self.view = view
        self.get_nutrient_data = get_nutrient_data
        self.on_nutrient_qty_changed = on_nutrient_qty_changed
        # Bring in a search view controller to handle the search column
        self.search_column_ctrl = SearchColumnCtrl(
            view=self.view.search_column,
            get_searchable_strings=lambda: list(get_nutrient_data().keys()),
            on_result_selected=lambda i : None, # No action required.
        )
        # Load the nutrient quantities
        self.load_nutrient_quantities()

    def add_nutrient_quantity(
        self, nutrient_quantity: IngredientNutrientQuantity
    ) -> None:
        """Add a new nutrient quantity to the view."""
        # Create a new nutrient editor view
        nutr_qty = NutrientQuantityEditorView(
            parent=self.view,
            nutrient_name=nutrient_quantity.nutrient_name,
        )
        # Connect signals
        nutr_qty.nutrientMassChanged.connect(self.on_nutrient_qty_changed)
        nutr_qty.nutrientMassUnitsChanged.connect(self.on_nutrient_qty_changed)
        # Add the nutrient editor to the view
        self.view.search_column.add_result(nutr_qty)

    def load_nutrient_quantities(self) -> None:
        """Fetches the ingredient quantities data and loads it into the view."""
        # Get the nutrient data
        nutrient_data = self.get_nutrient_data()
        # Load the data into the view
        for nutrient_name, nutrient_quantity in nutrient_data.items():
            self.add_nutrient_quantity(nutrient_quantity)
