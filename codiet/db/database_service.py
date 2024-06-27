from typing import Any

from codiet.utils.map import BidirectionalMap
from codiet.db.repository import Repository
from codiet.models.units import Unit
from codiet.models.ingredients import (
    Ingredient, IngredientQuantity
)
from codiet.models.nutrients import (
    IngredientNutrientQuantity,
)
from codiet.models.units import IngredientUnitConversion
from codiet.models.time import RecipeServeTimeWindow
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

    def create_global_nutrients(
        self, nutrient_data: dict[str, Any], parent_id: int | None = None
    ) -> None:
        """Recursively adds nutrients and their aliases into the database.
        Designed to accept the nested dictionary structure defined in the
        JSON config file.
        Args:
            nutrient_data (dict[str, Any]): The nutrient data to insert.
            parent_id (int|None): The parent nutrient ID.
        """
        for nutrient_name, nutrient_info in nutrient_data.items():
            # Insert the nutrient
            nutrient_id = self.repository.create_global_nutrient(
                name=nutrient_name, parent_id=parent_id
            )
            # Insert the aliases for the nutrient
            for alias in nutrient_info.get("aliases", []):
                self.repository.create_nutrient_alias(
                    alias=alias, primary_nutrient_id=nutrient_id
                )
            # Recursively insert the child nutrients
            if "children" in nutrient_info:
                self.create_global_nutrients(
                    nutrient_info["children"], parent_id=nutrient_id
                )

    def create_global_recipe_tags(self, tag_data: dict[str, dict]) -> None:
        """Insert the global recipe tags into the database.
        Works through the tree structure provided in tag data and inserts
        the tags into the database.
        Args:
            tag_data (dict[str, dict]): The recipe tag data from the
                JSON config file.
        Returns:
            None
        """

        def insert_tags(data: dict[str, dict], parent_id: int | None = None) -> None:
            for tag_name, children in data.items():
                # Insert the current tag and get its ID
                tag_id = self.repository.create_global_recipe_tag(tag_name, parent_id)
                # Recursively insert children tags
                if children:
                    insert_tags(children, tag_id)

        # Start the recursive insertion with the root tags
        insert_tags(tag_data)

    def create_empty_ingredient(self, ingredient_name: str) -> Ingredient:
        """Creates an ingredient."""
        # Insert the ingredient name into the database
        ingredient_id = self.repository.create_ingredient_name(ingredient_name)
        # Init the ingredient
        ingredient = Ingredient(ingredient_name, ingredient_id)
        # Return the ingredient
        return ingredient

    def create_ingredient_unit_conversion(
        self,
        ingredient_id: int,
        from_unit_id: int,
        from_unit_qty: float,
        to_unit_id: int,
        to_unit_qty: float,
    ) -> IngredientUnitConversion:
        """Creates a unit conversion for the given ingredient.
        Args:
            ingredient_id (int): The id of the ingredient.
            from_unit_id (int): The id of the unit to convert from.
            from_unit_qty (float): The quantity of the from unit.
            to_unit_id (int): The id of the unit to convert to.
            to_unit_qty (float): The quantity of the to unit.
        Returns:
            IngredientUnitConversion: The created unit conversion.
        """
        # Raise an exception if there is an equivalent conversion already
        # defined for this ingredient. Do this by checking for matching
        # from and to units. Treat this bidirectionally.
        existing_conversions = self.read_ingredient_unit_conversions(ingredient_id)
        for conversion in existing_conversions.values():
            if (
                conversion.from_unit_id == from_unit_id
                and conversion.to_unit_id == to_unit_id
            ):
                raise KeyError("Unit conversion already exists for this ingredient.")
            if (
                conversion.from_unit_id == to_unit_id
                and conversion.to_unit_id == from_unit_id
            ):
                raise KeyError("Unit conversion already exists for this ingredient.")
        # Insert the unit conversion into the database
        conversion_id = self.repository.create_ingredient_unit_conversion(
            ingredient_id=ingredient_id,
            from_unit_id=from_unit_id,
            from_unit_qty=from_unit_qty,
            to_unit_id=to_unit_id,
            to_unit_qty=to_unit_qty,
        )
        # Init the unit conversion
        unit_conversion = IngredientUnitConversion(
            ingredient_id=ingredient_id,
            id=conversion_id,
            from_unit_id=from_unit_id,
            from_unit_qty=from_unit_qty,
            to_unit_id=to_unit_id,
            to_unit_qty=to_unit_qty,
        )
        # Return the unit conversion
        return unit_conversion

    def create_ingredient_nutrient_quantity(
        self,
        ingredient_id: int,
        nutrient_id: int,
        ntr_mass_value: float,
        ntr_mass_unit_id: int,
        ing_qty_value: float,
        ing_qty_unit_id: int,
    ) -> IngredientNutrientQuantity:
        """Creates a nutrient quantity for the given ingredient.
        Args:
            ingredient_id (int): The id of the ingredient.
            nutrient_id (int): The id of the nutrient.
            ntr_mass_value (float): The mass value of the nutrient.
            ntr_mass_unit_id (int): The unit id of the mass value.
            ing_qty_value (float): The quantity value of the ingredient.
            ing_qty_unit_id (int): The unit id of the quantity value.
        Returns:
            IngredientNutrientQuantity: The created nutrient quantity.
        """
        # Insert the nutrient quantity into the database
        nutrient_quantity_id = self.repository.create_ingredient_nutrient_quantity(
            ingredient_id=ingredient_id,
            nutrient_id=nutrient_id,
            ntr_mass_value=ntr_mass_value,
            ntr_mass_unit_id=ntr_mass_unit_id,
            ing_qty_value=ing_qty_value,
            ing_qty_unit_id=ing_qty_unit_id,
        )
        # Init the nutrient quantity
        nutrient_quantity = IngredientNutrientQuantity(
            id=nutrient_quantity_id,
            nutrient_id=nutrient_id,
            ingredient_id=ingredient_id,
            ntr_mass_value=ntr_mass_value,
            ntr_mass_unit_id=ntr_mass_unit_id,
            ing_qty_value=ing_qty_value,
            ing_qty_unit_id=ing_qty_unit_id,
        )
        # Return the nutrient quantity
        return nutrient_quantity

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

    def create_recipe_serve_time_window(
        self, recipe_id: int, window_string: str
    ) -> RecipeServeTimeWindow:
        """Creates a serve time window for the given recipe.
        Args:
            recipe_id (int): The id of the recipe.
            window_string (str): The string representing the time window.
        Returns:
            RecipeServeTimeWindow: The created serve time window.
        """
        # Insert the serve time window into the database
        id = self.repository.create_recipe_serve_time_window(recipe_id, window_string)
        # Init the serve time window
        serve_time_window = RecipeServeTimeWindow(
            id=id, recipe_id=recipe_id, window_string=window_string
        )
        return serve_time_window

    def create_recipe_ingredient_quantity(
        self,
        recipe_id: int,
        ingredient_id: int,
        qty_unit_id: int|None,
        qty_value: float|None,
        qty_ltol: float|None,
        qty_utol: float|None,
    ) -> IngredientQuantity:
        """Creates an ingredient quantity for the given recipe.
        Args:
            recipe_id (int): The id of the recipe.
            ingredient_id (int): The id of the ingredient.
            qty_unit_id (int|None): The unit id of the quantity.
            qty_value (float|None): The value of the quantity.
            qty_ltol (float|None): The lower tolerance of the quantity.
            qty_utol (float|None): The upper tolerance of the quantity.
        Returns:
            IngredientQuantity: The created ingredient quantity.
        """
        # Insert the ingredient quantity into the database
        id = self.repository.create_recipe_ingredient_quantity(
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            qty_unit_id=qty_unit_id,
            qty_value=qty_value,
            qty_ltol=qty_ltol,
            qty_utol=qty_utol,
        )
        # Init the ingredient quantity
        ingredient_quantity = IngredientQuantity(
            id=id,
            ingredient_id=ingredient_id,
            recipe_id=recipe_id,
            qty_unit_id=qty_unit_id,
            qty_value=qty_value,
            qty_ltol=qty_ltol,
            qty_utol=qty_utol,
        )
        return ingredient_quantity

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
            unit_name_id_map.add_mapping(integer=unit_id, string=unit_data["unit_name"])
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
            flag_name_id_map.add_mapping(integer=flag_id, string=flag_name)
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
                integer=nutrient_id, string=nutrient_data["nutrient_name"]
            )
        return nutrient_name_id_map

    def build_recipe_tag_name_id_map(self) -> BidirectionalMap:
        """Fetches a bidirectional map of recipe tag names to IDs.
        Returns:
            BidirectionalMap: A bidirectional map of recipe tag names to IDs.
        """
        # Fetch all the recipe tags
        recipe_tags = self.repository.read_all_global_recipe_tags()
        # Create a bidirectional map
        recipe_tag_name_id_map = BidirectionalMap()
        # Add each recipe tag to the map
        for tag_id, tag_name in recipe_tags.items():
            recipe_tag_name_id_map.add_mapping(integer=tag_id, string=tag_name)
        return recipe_tag_name_id_map

    def build_ingredient_name_id_map(self) -> BidirectionalMap:
        """Fetches a bidirectional map of ingredient names to IDs.
        Returns:
            BidirectionalMap: A bidirectional map of ingredient names to IDs.
        """
        # Fetch all the ingredients
        ingredients = self.repository.read_all_ingredient_names()
        # Create a bidirectional map
        ingredient_name_id_map = BidirectionalMap()
        # Add each ingredient to the map
        for ingredient_id, ingredient_name in ingredients.items():
            ingredient_name_id_map.add_mapping(
                integer=ingredient_id, string=ingredient_name
            )
        return ingredient_name_id_map

    def read_global_unit(self, unit_id: int) -> Unit:
        """Returns the unit with the given ID.
        Args:
            unit_id (int): The id of the unit.
            
        Returns:
            Unit: The unit with the given ID.
        """
        # Fetch the data for all the units
        all_units_data = self.repository.read_all_global_units()
        # Fetch the aliases for this specific unit
        aliases = self.repository.read_global_unit_aliases(unit_id)
        # Init a fresh unit instance
        unit = Unit(
            id=unit_id,
            unit_name=all_units_data[unit_id]["unit_name"],
            single_display_name=all_units_data[unit_id]["single_display_name"],
            plural_display_name=all_units_data[unit_id]["plural_display_name"],
            type=all_units_data[unit_id]["unit_type"],
            aliases=aliases,
        )
        return unit

    def read_all_global_units(self) -> dict[int, Unit]:
        """Returns all the global units.
        Returns:
            dict[int, Unit]: A dictionary of global units, where the key is the
            id of each specific unit.
        """
        # Fetch the data for all the units
        all_units_data = self.repository.read_all_global_units()
        # Init a dict to hold the units
        units = {}
        # Cycle through the raw data
        for unit_id, unit_data in all_units_data.items():
            # Create a new unit
            units[unit_id] = Unit(
                id=unit_id,
                unit_name=unit_data["unit_name"],
                single_display_name=unit_data["single_display_name"],
                plural_display_name=unit_data["plural_display_name"],
                type=unit_data["unit_type"],
                aliases=unit_data["aliases"],
            )
        return units

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
        ingredient.description = self.repository.read_ingredient_description(
            ingredient.id
        )
        # Fetch the cost data
        cost_data = self.repository.read_ingredient_cost(ingredient.id)
        ingredient.cost_value = cost_data["cost_value"]
        ingredient.cost_qty_unit_id = cost_data["cost_qty_unit_id"]
        ingredient.cost_qty_value = cost_data["cost_qty_value"]
        # Fetch the standard unit
        ingredient.standard_unit_id = self.repository.read_ingredient_standard_unit_id(
            ingredient.id
        )
        # Fetch the unit conversions
        ingredient._unit_conversions = self.read_ingredient_unit_conversions(
            ingredient_id=ingredient.id
        )
        # Fetch the flags
        ingredient._flags = self.repository.read_ingredient_flags(ingredient.id)
        # Fetch the GI
        ingredient.gi = self.repository.read_ingredient_gi(ingredient.id)
        # Fetch the nutrients
        ingredient._nutrient_quantities = self.read_ingredient_nutrient_quantities(
            ingredient_id=ingredient.id
        )
        # Return the completed ingredient
        return ingredient

    def read_ingredient_unit_conversions(
        self, ingredient_id: int
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
        raw_conversion_data = self.repository.read_ingredient_unit_conversions(
            ingredient_id
        )
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
                id=nutrient_qty_data["id"],
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
        self.repository.update_ingredient_description(
            ingredient.id, ingredient.description
        )
        # Update the cost data
        self.repository.update_ingredient_cost(
            ingredient_id=ingredient.id,
            cost_value=ingredient.cost_value,
            cost_qty_unit_id=ingredient.cost_qty_unit_id,
            cost_qty_value=ingredient.cost_qty_value,
        )
        # Update the standard unit
        self.repository.update_ingredient_standard_unit_id(
            ingredient.id, ingredient.standard_unit_id
        )
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
