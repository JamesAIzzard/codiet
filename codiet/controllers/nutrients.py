from typing import Callable

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
            on_result_selected=lambda i: None,  # No action required.
        )

    def make_nutrient_quantity_view(
        self,
        nutrient_name: str | None = None,
        nutrient_quantity: IngredientNutrientQuantity | None = None,
    ) -> NutrientQuantityEditorView:
        """Create a new nutrient quantity editor view."""
        if nutrient_name is None and nutrient_quantity is None:
            raise ValueError(
                "Either nutrient_name or nutrient_quantity must be provided."
            )
        # If a nutrient quantity is not provided, use the name.
        if nutrient_quantity is None:
            assert nutrient_name is not None
            nutr_qty_view = NutrientQuantityEditorView(nutrient_name=nutrient_name)
        # Otherwise, use the nutrient quantity object.
        else:
            nutr_qty_view = NutrientQuantityEditorView(
                parent=self.view,
                nutrient_name=nutrient_quantity.nutrient_name,
            )
            # Set the nutrient mass
            nutr_qty_view.update_nutrient_mass(nutrient_quantity.nutrient_mass)
            nutr_qty_view.update_nutrient_mass_units(
                nutrient_quantity.nutrient_mass_unit
            )
        # Connect signals
        nutr_qty_view.nutrientMassChanged.connect(self.on_nutrient_qty_changed)
        nutr_qty_view.nutrientMassUnitsChanged.connect(self.on_nutrient_qty_changed)
        return nutr_qty_view

    def add_nutrient_quantity(
        self, nutrient_quantity: IngredientNutrientQuantity
    ) -> None:
        """Add a new nutrient quantity to the view."""
        # Create a new nutrient editor view
        nutr_qty = self.make_nutrient_quantity_view(nutrient_quantity=nutrient_quantity)
        # Add the nutrient editor to the view
        self.view.search_column.add_result(nutr_qty)

    def load_nutrient_quantities(self) -> None:
        """Fetches the ingredient quantities data and loads it into the view."""
        # Get the nutrient data
        nutrient_data = self.get_nutrient_data()
        # Load the data into the view
        for nutrient_quantity in nutrient_data.values():
            self.add_nutrient_quantity(nutrient_quantity)
