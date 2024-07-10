from typing import Callable

from codiet.utils.map import BidirectionalMap
from codiet.models.nutrients import Nutrient, IngredientNutrientQuantity
from codiet.models.units import Unit
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
        available_mass_units: dict[int, Unit],        
        get_ingredient_nutrient_data: Callable[
            [], dict[int, IngredientNutrientQuantity]
        ],
        on_nutrient_qty_changed: Callable[[IngredientNutrientQuantity], None],
        scale_1g_to_new_unit: Callable[[int], float],
    ) -> None:
        """Initialise the NutrientQuantitiesEditorCtrl object.
        
        Args:
            view (NutrientQuantitiesEditorView): The view object.
            global_leaf_nutrients (dict[int, Nutrient]): A dictionary of global leaf nutrients.
            available_mass_units (dict[int, Unit]): A dictionary of available mass units.            
            get_ingredient_nutrient_data (Callable[[], dict[int, IngredientNutrientQuantity]]): A function that returns the nutrient data for the ingredient.
            on_nutrient_qty_changed (Callable[[IngredientNutrientQuantity], None]): A function to call when a nutrient quantity is changed.
            scale_1g_to_new_unit (Callable[[int], float]): A function to scale 1g to a new unit.
        
        global_leaf_nutrients:
            int: The nutrient id.
            Nutrient: The nutrient object.

        available_mass_units:
            int: The unit id.
            Unit: The unit object.
                        
        get_ingredient_nutrient_data:
            int: The nutrient id.
            IngredientNutrientQuantity: The nutrient quantity data.
        
        scale_1g_to_new_unit:
            int: The new unit id.
            float: The conversion factor.
        """
        self.view = view
        self._global_leaf_nutrients = global_leaf_nutrients
        self._available_mass_units = available_mass_units
        self._get_ingredient_nutrient_data = get_ingredient_nutrient_data
        self._on_nutrient_qty_changed_callback = on_nutrient_qty_changed
        self._scale_1g_to_new_unit = scale_1g_to_new_unit
        # Find the gram unit ID
        self._gram_unit_id = next(
            unit_id
            for unit_id, unit in available_mass_units.items()
            if unit.unit_name == "gram"
        )

        # Create a map between leaf nutrient names and id's
        self.leaf_nutrient_name_id_map = BidirectionalMap()
        for nutrient_id, nutrient in global_leaf_nutrients.items():
            self.leaf_nutrient_name_id_map.add_mapping(
                nutrient.nutrient_name, nutrient_id
            )

        # Create a dict of the form {unit_id: unit_display_name} for
        # the available mass units
        self._mass_unit_id_to_display_name = {
            unit_id: unit.plural_display_name for unit_id, unit in available_mass_units.items()
        }

        # Bring in a search view controller to handle the search column
        self.search_column_ctrl = SearchColumnCtrl(
            view=self.view.display_column,
            get_view_item_and_data_for_string=self._get_nutrient_quantity_view_and_id_for_nutrient_name,
            get_searchable_strings=lambda: self.leaf_nutrient_name_id_map.str_values,
            on_result_selected=lambda item: None,  # No action required.
        )

    def rescale_nutrient_quantities(
        self, ingredient_ref_qty: float, ingredient_ref_unit_id: int
    ) -> None:
        """Rescale the nutrient quantities based on a new ingredient quantity.
        The nutrient quantities are defined against a reference quantity of ingredient
        measured in grams. Each nutrient quantity is defined against this reference.
        When the user changes the ingredient reference quantity in the view, we need to
        rescale the nutrient quantities to match the new reference quantity.
        Args:
            ingredient_ref_qty (float): The new ingredient quantity.
            ingredient_ref_unit_id (int): The new ingredient quantity unit id.
        """
        # Get the nutrient data
        nutrient_data = self._get_ingredient_nutrient_data()
        # For each nutrient editor view,
        for nutrient_id, nutrient_qty in nutrient_data.items():
            # If there is no reference quantity for this nutrient, or the nutrient
            # quantity is not set, skip it.
            if (
                nutrient_qty.ing_grams_value is None
                or nutrient_qty.nutrient_mass_value is None
            ):
                continue
            # Calculate the individual conversion factor based on the reference
            # quantity used in this nutrient quantity.
            conv_factor_1g = (
                nutrient_qty.ing_grams_value * self._scale_1g_to_new_unit(ingredient_ref_unit_id)
            )
            conv_factor = ingredient_ref_qty * conv_factor_1g
            # Calculate the new mass
            new_mass = nutrient_qty.nutrient_mass_value * conv_factor
            # Grab the view
            view_item: NutrientQuantityEditorView = self.search_column_ctrl.view.lst_search_results.get_view_item_for_data(nutrient_id)  # type: ignore
            # Write the new mass to the view
            view_item.nutrient_mass_value = new_mass

    def add_nutrient_quantity(
        self, nutrient_quantity: IngredientNutrientQuantity
    ) -> None:
        """Add a new nutrient quantity to the view.
        Args:
            nutrient_quantity (IngredientNutrientQuantity): The nutrient quantity to add to the view.
        Returns:
            None
        """
        # Create the view for the nutrient quantity
        nutr_qty = self._make_nutrient_quantity_view(
            nutrient_quantity=nutrient_quantity
        )
        # Add the view to the search column
        self.view.display_column.lst_search_results.add_item(
            item_content=nutr_qty, data=nutrient_quantity.nutrient_id
        )

    def set_nutrient_quantities(
        self, nutrient_quantities: dict[int, IngredientNutrientQuantity]
    ) -> None:
        """Fetches the ingredient quantities data and loads it into the view.

        Args:
            nutrient_quantities (dict[int, IngredientNutrientQuantity]): A dictionary of nutrient quantities to load into the view.
                int: The nutrient global id.
                IngredientNutrientQuantity: The nutrient quantity data to load into the view.
        """
        # Clear the existing data
        self.search_column_ctrl.reset_search()
        for nutrient_quantity in nutrient_quantities.values():
            self.add_nutrient_quantity(nutrient_quantity)

    def _on_nutrient_mass_changed(
        self, nutrient_id: int, nutrient_mass: float | None
    ) -> None:
        """Handle a nutrient mass being changed."""
        # Grab the nutrient quantity
        nutrient_data = self._get_ingredient_nutrient_data()[nutrient_id]
        # Update the mass
        nutrient_data.nutrient_mass_value = nutrient_mass
        # Call the callback
        self._on_nutrient_qty_changed_callback(nutrient_data)

    def _on_nutrient_mass_unit_changed(
        self, nutrient_id: int, nutrient_mass_unit_id: int
    ) -> None:
        """Handle a nutrient quantity unit being changed."""
        # Grab the nutrient quantity
        nutrient_data = self._get_ingredient_nutrient_data()[nutrient_id]
        # Update the mass unit
        nutrient_data.nutrient_mass_unit_id = nutrient_mass_unit_id
        # Call the callback
        self._on_nutrient_qty_changed_callback(nutrient_data)

    def _get_nutrient_quantity_view_and_id_for_nutrient_name(
        self, nutrient_name: str
    ) -> tuple[NutrientQuantityEditorView, int]:
        """Converts a nutrient name into a nutrient quantity view and id.
        Args:
            nutrient_name (str): The name of the nutrient to convert.
        Returns:
            tuple[NutrientQuantityEditorView, int]: The nutrient quantity view and the nutrient id.
        """
        # Get the nutrient id
        nutrient_id = self.leaf_nutrient_name_id_map.get_int(nutrient_name)
        # Get the nutrient quantity
        nutrient_qty = self._get_ingredient_nutrient_data()[nutrient_id]
        # Create the view
        view = self._make_nutrient_quantity_view(nutrient_qty)
        return view, nutrient_id

    def _make_nutrient_quantity_view(
        self,
        nutrient_quantity: IngredientNutrientQuantity,
    ) -> NutrientQuantityEditorView:
        """Create a new nutrient quantity editor view."""
        # Create the view
        nutr_qty_view = NutrientQuantityEditorView(
            parent=self.view,
            global_nutrient_id=nutrient_quantity.nutrient_id,
            nutrient_name=self._global_leaf_nutrients[
                nutrient_quantity.nutrient_id
            ].nutrient_name,
            nutrient_mass_value=nutrient_quantity.nutrient_mass_value,
            available_mass_units=self._mass_unit_id_to_display_name,
            selected_mass_unit_id=nutrient_quantity.nutrient_mass_unit_id,
        )
        # Connect signals
        nutr_qty_view.nutrientMassChanged.connect(self._on_nutrient_mass_changed)
        nutr_qty_view.nutrientMassUnitsChanged.connect(
            self._on_nutrient_mass_unit_changed
        )
        return nutr_qty_view
