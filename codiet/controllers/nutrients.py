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
            get_result_for_string=self._make_nutrient_quantity_view,
            get_searchable_strings=lambda: list(get_nutrient_data().keys()),
            on_result_selected=lambda item: None,  # No action required.
        )

    def add_nutrient_quantity(
        self, nutrient_quantity: IngredientNutrientQuantity
    ) -> None:
        """Add a new nutrient quantity to the view."""
        # Create the view for the nutrient quantity
        nutr_qty = self._make_nutrient_quantity_view(nutrient_quantity=nutrient_quantity)
        # Add the view to the search column
        self.view.search_column.results_list.add_item(nutr_qty)

    def load_all_nutrient_quantities(self) -> None:
        """Fetches the ingredient quantities data and loads it into the view."""
        # Clear the existing data
        self.search_column_ctrl.reset_search()
        # Get the nutrient data
        nutrient_data = self.get_nutrient_data()
        # Load the data into the view
        for nutrient_quantity in nutrient_data.values():
            self.add_nutrient_quantity(nutrient_quantity)
    
    def _on_nutrient_mass_changed(self, nutrient_name:str, nutrient_mass: float|None) -> None:
        """Handle a nutrient mass being changed."""
        # Grab the nutrient quantity
        nutrient_data = self.get_nutrient_data()[nutrient_name]
        # Update the mass
        nutrient_data.nutrient_mass = nutrient_mass
        # Call the callback
        self.on_nutrient_qty_changed(nutrient_data)
    
    def _on_nutrient_mass_unit_changed(self, nutrient_name: str, nutrient_mass_unit: str) -> None:
        """Handle a nutrient quantity unit being changed."""
        # Grab the nutrient quantity
        nutrient_data = self.get_nutrient_data()[nutrient_name]
        # Update the mass unit
        nutrient_data.nutrient_mass_unit = nutrient_mass_unit
        # Call the callback
        self.on_nutrient_qty_changed(nutrient_data)

    def _make_nutrient_quantity_view(
        self,
        nutrient_name: str | None = None,
        nutrient_quantity: IngredientNutrientQuantity | None = None,
    ) -> NutrientQuantityEditorView:
        """Create a new nutrient quantity editor view."""
        if nutrient_name is None and nutrient_quantity is None:
            raise ValueError(
                "Either nutrient_name or nutrient_quantity must be provided."
            )
        # If a nutrient quantity is not provided, use the name to fetch
        # the required data.
        if nutrient_quantity is None:
            assert nutrient_name is not None
            # Grab the data for the nutrient quantity
            nutrient_quantity = self.get_nutrient_data()[nutrient_name]
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
        nutr_qty_view.nutrientMassChanged.connect(self._on_nutrient_mass_changed)
        nutr_qty_view.nutrientMassUnitsChanged.connect(self._on_nutrient_mass_unit_changed)
        return nutr_qty_view    