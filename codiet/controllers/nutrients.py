from typing import Callable

from codiet.utils.map import BidirectionalMap
from codiet.db.database_service import DatabaseService
from codiet.models.nutrients import Nutrient, IngredientNutrientQuantity
from codiet.views.nutrients import (
    NutrientQuantitiesEditorView,
    NutrientQuantityEditorView,
)
from codiet.controllers.search import SearchColumnCtrl


class NutrientQuantitiesEditorCtrl:
    def __init__(
        self,
        view: NutrientQuantitiesEditorView,
        global_leaf_nutrients: dict[int, Nutrient],
        get_ingredient_nutrient_data: Callable[[], dict[int, IngredientNutrientQuantity]],
        on_nutrient_qty_changed: Callable[[IngredientNutrientQuantity], None],
    ) -> None:
        self.view = view
        self.global_leaf_nutrients = global_leaf_nutrients

        # Create a map between leaf nutrient names and id's
        self.leaf_nutrient_name_id_map = BidirectionalMap()
        for nutrient_id, nutrient in global_leaf_nutrients.items():
            self.leaf_nutrient_name_id_map.add_mapping(nutrient.nutrient_name, nutrient_id)

        self.get_ingredient_nutrient_data = get_ingredient_nutrient_data
        self.on_nutrient_qty_changed_callback = on_nutrient_qty_changed

        # Bring in a search view controller to handle the search column
        self.search_column_ctrl = SearchColumnCtrl(
            view=self.view.search_column,
            get_view_item_and_data_for_string=self._get_nutrient_quantity_view_for_nutrient_name,
            get_searchable_strings=lambda: self.leaf_nutrient_name_id_map.str_values,
            on_result_selected=lambda item: None,  # No action required.
        )

    def rescale_nutrient_quantities(self, conversion_factor: float) -> None:
        """Rescale the nutrient quantities based on a new ingredient quantity."""
        # Get the nutrient data
        nutrient_data = self.get_ingredient_nutrient_data()
        # Rescale the nutrient quantities
        for nutrient_quantity in nutrient_data.values():
            nutrient_quantity.ingredient_quantity_value = new_quantity
            self.on_nutrient_qty_changed_callback(nutrient_quantity)

    def add_nutrient_quantity(
        self, nutrient_quantity: IngredientNutrientQuantity
    ) -> None:
        """Add a new nutrient quantity to the view."""
        # Create the view for the nutrient quantity
        nutr_qty = self._make_nutrient_quantity_view(
            nutrient_quantity=nutrient_quantity
        )
        # Add the view to the search column
        self.view.search_column.results_list.add_item(nutr_qty)

    def load_all_nutrient_quantities(self) -> None:
        """Fetches the ingredient quantities data and loads it into the view."""
        # Clear the existing data
        self.search_column_ctrl.reset_search()
        # Get the nutrient data
        nutrient_data = self.get_ingredient_nutrient_data()
        # Load the data into the view
        for nutrient_quantity in nutrient_data.values():
            self.add_nutrient_quantity(nutrient_quantity)

    def _on_nutrient_mass_changed(
        self, nutrient_id: int, nutrient_mass: float | None
    ) -> None:
        """Handle a nutrient mass being changed."""
        # Grab the nutrient quantity
        nutrient_data = self.get_ingredient_nutrient_data()[nutrient_id]
        # Update the mass
        nutrient_data.nutrient_mass_value = nutrient_mass
        # Call the callback
        self.on_nutrient_qty_changed_callback(nutrient_data)

    def _on_nutrient_mass_unit_changed(
        self, nutrient_id: int, nutrient_mass_unit: str
    ) -> None:
        """Handle a nutrient quantity unit being changed."""
        # Grab the nutrient quantity
        nutrient_data = self.get_ingredient_nutrient_data()[nutrient_id]
        # Update the mass unit
        nutrient_data.nutrient_mass_unit = nutrient_mass_unit
        # Call the callback
        self.on_nutrient_qty_changed_callback(nutrient_data)

    def _get_nutrient_quantity_view_for_nutrient_name(self, nutrient_name:str) -> NutrientQuantityEditorView:
        """Get the nutrient quantity view for a given nutrient name."""
        # Get the nutrient id
        nutrient_id = self.leaf_nutrient_name_id_map.get_int(nutrient_name)
        # Get the nutrient quantity
        nutrient_data = self.get_ingredient_nutrient_data()[nutrient_id]
        # Create the view
        return self._make_nutrient_quantity_view(nutrient_data)

    def _make_nutrient_quantity_view(
        self,
        nutrient_quantity: IngredientNutrientQuantity,
    ) -> NutrientQuantityEditorView:
        """Create a new nutrient quantity editor view."""
        # Create the view
        nutr_qty_view = NutrientQuantityEditorView(
            parent=self.view,
            global_nutrient_id=nutrient_quantity.nutrient_id,
            nutrient_name=self.global_leaf_nutrients[nutrient_quantity.nutrient_id].nutrient_name,
            nutrient_mass_value=nutrient_quantity.nutrient_mass_value,
            available_mass_units=...,
            selected_mass_unit_id=...,
        )
        # Connect signals
        nutr_qty_view.nutrientMassChanged.connect(self._on_nutrient_mass_changed)
        nutr_qty_view.nutrientMassUnitsChanged.connect(
            self._on_nutrient_mass_unit_changed
        )
        return nutr_qty_view
