from typing import Any

from codiet.utils.map import BidirectionalMap
from codiet.db.repository import Repository
from codiet.models.ingredients import (
    Ingredient,
)
from codiet.models.nutrients import (
    IngredientNutrientQuantity,
)
from codiet.models.units import IngredientUnitConversion
from codiet.models.recipes import Recipe

class DatabaseService:
    """Service for interacting with the database."""

    def __init__(self, repository: Repository):
        self._repo = repository

    @property
    def repository(self) -> Repository:
        return self._repo

    def create_global_units(self, units: dict[str, Any]) -> None:
        """Insert the global units into the database.
        Designed to accept the dictionary structure defined in the 
        JSON config file.
        Args:
            units (dict[str, Any]): A dictionary of unit data.
        """
        # First, insert each unit and its alias
        for unit_name, unit_info in units.items():
            # Insert the unit
            unit_id = self.repository.create_global_unit(
                unit_name=unit_name,
                unit_type=unit_info["type"],
                single_display_name=unit_info["single_display_name"],
                plural_display_name=unit_info["plural_display_name"],
            )
            # Insert the aliases for the unit
            for alias in unit_info.get("aliases", []):
                self.repository.create_global_unit_alias(
                    alias=alias,
                    unit_id=unit_id,
                )
        # Read the names of all units
        unit_name_id_map = self.build_unit_name_id_map()
        # Then, insert the conversion factors
        for unit_name, unit_info in units.items():
            # For each conversion factor
            for to_unit_name, factor in unit_info["conversions"].items():
                # Get the id of the to unit
                to_unit_id = unit_name_id_map.get_int(to_unit_name)
                # Insert the conversion factor
                self.repository.create_global_unit_conversion(
                    from_unit_id=unit_name_id_map.get_int(unit_name),
                    to_unit_id=to_unit_id,
                    from_unit_qty=1.0,
                    to_unit_qty=factor,
                )

    def create_global_flags(self, flags: list[str]) -> None:
        """Insert the global flags into the database.
        Designed to accept the list of strings defined in the 
        JSON config file.
        Args:
            flags (list[str]): A list of flag names.
        """
        for flag in flags:
            self.repository.create_global_flag(flag)

    def create_global_nutrients(self, nutrient_data: dict[str, Any], parent_id: int|None=None) -> None:
        """Recursively adds nutrients and their aliases into the database.
        Designed to accept the nested dictionary structure defined in the
        JSON config file.
        Args:
            nutrient_data (dict[str, Any]): The nutrient data to insert.
            parent_id (int|None): The parent nutrient ID.
        """
        for nutrient_name, nutrient_info in nutrient_data.items():
            # Insert the nutrient
            nutrient_id = self.repository.create_global_nutrient(name=nutrient_name, parent_id=parent_id)
            # Insert the aliases for the nutrient
            for alias in nutrient_info.get("aliases", []):
                self.repository.create_nutrient_alias(alias=alias, primary_nutrient_id=nutrient_id)
            # Recursively insert the child nutrients
            if "children" in nutrient_info:
                self.create_global_nutrients(nutrient_info["children"], parent_id=nutrient_id)

    def create_empty_ingredient(self, ingredient_name: str) -> Ingredient:
        """Creates an ingredient."""
        # Insert the ingredient name into the database
        ingredient_id = self.repository.create_ingredient_name(ingredient_name)
        # Init the ingredient
        ingredient = Ingredient(ingredient_name, ingredient_id)
        # Return the ingredient
        return ingredient

    def create_empty_recipe(self, recipe_name: str) -> Recipe:
        """Creates an empty recipe with the given name."""
        # Insert the recipe name into the database
        recipe_id = self.repository.create_recipe_name(recipe_name)
        # Init the recipe
        recipe = Recipe(
            recipe_name=recipe_name,
            recipe_id=recipe_id,
        )
        # Return the recipe
        return recipe

    def build_unit_name_id_map(self) -> BidirectionalMap:
        """Fetches a bidirectional map of unit names to IDs.
        Returns:
            BidirectionalMap: A bidirectional map of unit names to IDs.
        """
        # Fetch all the units
        units = self.repository.read_all_global_units()
        # Create a bidirectional map
        unit_name_id_map = BidirectionalMap()
        # Add each unit to the map
        for unit_id, unit_data in units.items():
            unit_name_id_map.add_mapping(
                integer=unit_id,
                string=unit_data["unit_name"]
            )
        return unit_name_id_map

    def build_flag_name_id_map(self) -> BidirectionalMap:
        """Fetches a bidirectional map of flag names to IDs.
        Returns:
            BidirectionalMap: A bidirectional map of flag names to IDs.
        """
        # Fetch all the flags
        flags = self.repository.read_all_global_flags()
        # Create a bidirectional map
        flag_name_id_map = BidirectionalMap()
        # Add each flag to the map
        for flag_id, flag_name in flags.items():
            flag_name_id_map.add_mapping(
                integer=flag_id,
                string=flag_name
            )
        return flag_name_id_map
    
    def build_nutrient_name_id_map(self) -> BidirectionalMap:
        """Fetches a bidirectional map of nutrient names to IDs.
        Returns:
            BidirectionalMap: A bidirectional map of nutrient names to IDs.
        """
        # Fetch all the nutrients
        nutrients = self.repository.read_all_global_nutrients()
        # Create a bidirectional map
        nutrient_name_id_map = BidirectionalMap()
        # Add each nutrient to the map
        for nutrient_id, nutrient_data in nutrients.items():
            nutrient_name_id_map.add_mapping(
                integer=nutrient_id,
                string=nutrient_data["nutrient_name"]
            )
        return nutrient_name_id_map

    def read_ingredient(self, ingredient_id: int) -> Ingredient:
        """Returns the ingredient with the given name.
        Args:
            ingredient_id (int): The id of the ingredient.
        Returns:
            Ingredient: The ingredient with the given id.
        """
        # Fetch the ingredient name corresponding to the id
        ingredient_name = self.repository.read_ingredient_name(ingredient_id)
        # Init a fresh ingredient instance
        ingredient = Ingredient(
            id=ingredient_id,
            name=ingredient_name,
        )
        # Fetch the description
        ingredient.description = self.repository.read_ingredient_description(ingredient.id)
        # Fetch the cost data
        cost_data = self.repository.read_ingredient_cost(ingredient.id)
        ingredient.cost_value = cost_data['cost_value']
        ingredient.cost_qty_unit_id = cost_data['cost_qty_unit_id']
        ingredient.cost_qty_value = cost_data['cost_qty_value']
        # Fetch the standard unit
        ingredient.standard_unit_id = self.repository.read_ingredient_standard_unit_id(ingredient.id)
        # Fetch the unit conversions
        ingredient._unit_conversions = self.read_ingredient_unit_conversions(ingredient_id=ingredient.id)
        # Fetch the flags
        ingredient._flags = self.repository.read_ingredient_flags(ingredient.id)
        # Fetch the GI
        ingredient.gi = self.repository.read_ingredient_gi(ingredient.id)
        # Fetch the nutrients
        ingredient._nutrient_quantities = self.read_ingredient_nutrient_quantities(ingredient_id=ingredient.id)
        # Return the completed ingredient
        return ingredient

    def read_ingredient_unit_conversions(
        self, 
        ingredient_id: int
    ) -> dict[int, IngredientUnitConversion]:
        """Returns a list of unit conversions for the given ingredient.
        Args:
            ingredient_id (int): The id of the ingredient.
        Returns:
            dict[int, IngredientUnitConversion]: A dictionary of custom units, where the key is the
            id of each specific unit conversion.
        """
        # Init a list to hold the custom units
        conversions = {}
        # Fetch the raw data from the repo
        raw_conversion_data = self.repository.read_ingredient_unit_conversions(ingredient_id)
        # Cycle through the raw data
        for conversion_id, conversion_data in raw_conversion_data.items():
            # Create a new custom unit
            conversions[conversion_id] = IngredientUnitConversion(
                ingredient_id=ingredient_id,
                id=conversion_id,
                from_unit_id=conversion_data["from_unit_id"],
                from_unit_qty=conversion_data["from_unit_qty"],
                to_unit_id=conversion_data["to_unit_id"],
                to_unit_qty=conversion_data["to_unit_qty"],
            )
        return conversions

    def read_ingredient_nutrient_quantities(
        self, ingredient_id: int
    ) -> dict[int, IngredientNutrientQuantity]:
        """Returns the nutrient quantities for the given ingredient.
        Args:
            ingredient_id (int): The id of the ingredient.
        Returns:
            dict[int, IngredientNutrientQuantity]: A dictionary of nutrient quantities, where the key is the
            id of each specific nutrient quantity.
        """
        # Init a dict to hold the nutrient quantities
        nutrient_quantities: dict[int, IngredientNutrientQuantity] = {}
        # Fetch the raw data from the repo
        raw_nutrient_quantities = self._repo.read_ingredient_nutrient_quantities(
            ingredient_id
        )
        # Cycle through the raw data
        for nutrient_id, nutrient_qty_data in raw_nutrient_quantities.items():
            # And add the data to the dict
            nutrient_quantities[nutrient_id] = IngredientNutrientQuantity(
                nutrient_id=nutrient_id,                
                ingredient_id=ingredient_id,
                ntr_mass_value=nutrient_qty_data["ntr_mass_value"],
                ntr_mass_unit_id=nutrient_qty_data["ntr_mass_unit_id"],
                ing_qty_value=nutrient_qty_data["ing_qty_value"],
                ing_qty_unit_id=nutrient_qty_data["ing_qty_unit_id"],
            )
        return nutrient_quantities

    def read_recipe(self, recipe_id: int) -> Recipe:
        """Returns the name of the recipe with the given ID."""
        raise NotImplementedError

    def update_ingredient(self, ingredient: Ingredient) -> None:
        """Updates the ingredient in the database."""
        # Update the name
        self.repository.update_ingredient_name(ingredient.id, ingredient.name)
        # Update the description
        self.repository.update_ingredient_description(ingredient.id, ingredient.description)
        # Update the cost data
        self.repository.update_ingredient_cost(
            ingredient_id=ingredient.id,
            cost_value=ingredient.cost_value,
            cost_qty_unit_id=ingredient.cost_qty_unit_id,
            cost_qty_value=ingredient.cost_qty_value,
        )
        # Update the standard unit
        self.repository.update_ingredient_standard_unit_id(ingredient.id, ingredient.standard_unit_id)
        # Update the unit conversions
        # First delete all the existing unit conversions
        self.repository.delete_ingredient_unit_conversions(ingredient.id)
        # Then add the new ones
        for unit_conversion in ingredient.unit_conversions.values():
            self.repository.create_ingredient_unit_conversion(
                ingredient_id=ingredient.id,
                from_unit_id=unit_conversion.from_unit_id,
                from_unit_qty=unit_conversion.from_unit_qty,
                to_unit_id=unit_conversion.to_unit_id,
                to_unit_qty=unit_conversion.to_unit_qty,
            )
        # Update the flags
        # First, remove all the flags
        self.repository.delete_ingredient_flags(ingredient.id)
        # Then add the new ones
        for flag_id, flag_value in ingredient.flags.items():
            self.repository.update_ingredient_flag(ingredient.id, flag_id, flag_value)
        # Update the GI
        self.repository.update_ingredient_gi(ingredient.id, ingredient.gi)
        # Update the nutrient quantities
        # First, remove all the nutrient quantities
        self.repository.delete_ingredient_nutrient_quantities(ingredient.id)
        # Then add the new ones
        for nutrient_quantity in ingredient.nutrient_quantities.values():
            self.repository.create_ingredient_nutrient_quantity(
                ingredient_id=ingredient.id,
                nutrient_id=nutrient_quantity.nutrient_id,
                ntr_mass_value=nutrient_quantity.nutrient_mass_value,
                ntr_mass_unit_id=nutrient_quantity.nutrient_mass_unit_id,
                ing_qty_value=nutrient_quantity.ingredient_quantity_value,
                ing_qty_unit_id=nutrient_quantity.ingredient_quantity_unit_id,
            )