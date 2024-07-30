from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

from codiet.utils.map import Map
from codiet.db.repository import Repository
from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import UnitConversion
from codiet.models.units.entity_unit_conversion import EntityUnitConversion
from codiet.models.nutrients import Nutrient
from codiet.models.ingredients.ingredient import Ingredient
from codiet.models.ingredients.ingredient_quantity import IngredientQuantity
from codiet.models.nutrients.entity_nutrient_quantity import (
    EntityNutrientQuantity,
)
from codiet.models.time import RecipeServeTimeWindow
from codiet.models.recipes.recipe import Recipe


class DatabaseService(QObject):
    """Service for interacting with the database."""

    ingredientIDNameChanged = pyqtSignal(object)

    def __init__(self, repository: Repository, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._repo = repository

        # Configure ingredient id-name caching and signalling
        self.ingredient_id_name_map: Map[int, str]
        self.cache_ingredient_name_id_map()

    @property
    def repository(self) -> Repository:
        return self._repo

    def cache_ingredient_name_id_map(self) -> Map[int, str]:
        """Re(generates) the cached ingredient name to ID map.
        Emits the ingredientIDNameChanged signal.
        Returns:
            Map: A bidirectional map of ingredient names to IDs.
        """
        # Init the map if doesn't exist
        if not hasattr(self, "ingredient_name_id_map"):
            self.ingredient_id_name_map = Map(one_to_one=True)
        # Fetch all the ingredients
        ingredients = self.repository.read_all_ingredient_names()
        # Clear the map
        self.ingredient_id_name_map.clear()
        # Add each ingredient to the map
        for ingredient_id, ingredient_name in ingredients.items():
            self.ingredient_id_name_map.add_mapping(key=ingredient_id, value=ingredient_name)
        # Emit the signal
        self.ingredientIDNameChanged.emit(self.ingredient_id_name_map)
        return self.ingredient_id_name_map

    def create_global_units(self, units: dict[str, Unit]) -> dict[int, Unit]:
        """Insert a dictionary of global units into the database.

        Args:
            units (dict[str, Units]): A dictionary of unit data.
        """
        # Init return dict
        persisted_units = {}
        # Insert each unit into the database
        for unit in units.values():
            persisted_unit = self.create_global_unit(unit)
            persisted_units[persisted_unit.id] = persisted_unit
        return persisted_units

    def create_global_unit(self, unit:Unit) -> Unit:
        """Creates a global unit."""
        # Insert the unit name into the database
        unit_id = self.repository.create_global_unit(
            unit_name=unit.unit_name,
            unit_type=unit.type,
            single_display_name=unit.single_display_name,
            plural_display_name=unit.plural_display_name,
        )
        # Insert the aliases for the unit
        for alias in unit.aliases:
            self.repository.create_global_unit_alias(
                alias=alias,
                unit_id=unit_id,
            )
        # Init the unit id
        unit.id = unit_id
        # Return the unit
        return unit

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

    def create_ingredient(self, ingredient: Ingredient) -> Ingredient:
        """Creates an ingredient in the database.
        Args:
            ingredient (Ingredient): The ingredient to create.
        Returns:
            Ingredient: The created ingredient.
        """
        # Insert the ingredient name into the database
        if ingredient.name is None:
            raise ValueError("Ingredient name must be set.")
        ingredient.id = self.repository.create_ingredient_name(ingredient.name)

        # Now we have an id, we can use the update method
        self.update_ingredient(ingredient)

        return ingredient

    def create_ingredient_unit_conversion(
        self,
        ingredient_id: int,
        from_unit_id: int,
        to_unit_id: int,
        to_unit_qty: float | None = None,
        from_unit_qty: float | None = None,
    ) -> EntityUnitConversion:
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
        unit_conversion = EntityUnitConversion(
            entity_id=ingredient_id,
            id=conversion_id,
            from_unit_id=from_unit_id,
            from_unit_qty=from_unit_qty,
            to_unit_id=to_unit_id,
            to_unit_qty=to_unit_qty,
        )
        # Return the unit conversion
        return unit_conversion

    def create_ingredient_nutrient_quantity(self, ing_nutr_qty: EntityNutrientQuantity) -> EntityNutrientQuantity:
        """Creates an entry for the ingredient nutrient quantity in the database.
        Returns the object, with the id populated.

        Args:
            ing_nutr_qty (EntityNutrientQuantity): The nutrient quantity object.
        Returns:
            EntityNutrientQuantity: The created nutrient quantity object.
        """
        # Raise an exception if the parent entity ID is not set
        if ing_nutr_qty.parent_entity_id is None:
            raise ValueError("The parent entity ID must be set.")
        # Insert the nutrient quantity into the database
        nutrient_quantity_id = self.repository.create_ingredient_nutrient_quantity(
            ingredient_id=ing_nutr_qty.parent_entity_id,
            global_nutrient_id=ing_nutr_qty.nutrient_id,
            ntr_mass_qty=ing_nutr_qty.nutrient_mass_value,
            ntr_mass_unit_id=ing_nutr_qty.nutrient_mass_unit_id,
            ing_grams_qty=ing_nutr_qty.entity_grams_value,
        )
        # Populate the ID and return the object
        ing_nutr_qty.id = nutrient_quantity_id
        return ing_nutr_qty

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
        qty_unit_id: int | None,
        qty_value: float | None,
        qty_ltol: float | None,
        qty_utol: float | None,
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

    def build_unit_name_id_map(self) -> Map[int, str]:
        """Fetches a bidirectional map of unit names to IDs.
        Returns:
            Map: A bidirectional map of unit ID's to names.
        """
        # Fetch all the units
        units = self.repository.read_all_global_units()
        # Create a bidirectional map
        unit_name_id_map: Map[int, str] = Map(one_to_one=True)
        # Add each unit to the map
        for unit_id, unit_data in units.items():
            unit_name_id_map.add_mapping(key=unit_id, value=unit_data["unit_name"])
        return unit_name_id_map

    def build_flag_name_id_map(self) -> Map[int, str]:
        """Fetches a bidirectional map of flag names to IDs.
        Returns:
            Map: A bidirectional map of flag names to IDs.
        """
        # Fetch all the flags
        flags = self.repository.read_all_global_flags()
        # Create a bidirectional map
        flag_name_id_map: Map[int, str] = Map(one_to_one=True)
        # Add each flag to the map
        for flag_id, flag_name in flags.items():
            flag_name_id_map.add_mapping(key=flag_id, value=flag_name)
        return flag_name_id_map

    def build_nutrient_name_id_map(self) -> Map[int, str]:
        """Fetches a bidirectional map of nutrient names to IDs.
        Returns:
            Map: A bidirectional map of nutrient names to IDs.
        """
        # Fetch all the nutrients
        nutrients = self.repository.read_all_global_nutrients()
        # Create a bidirectional map
        nutrient_name_id_map: Map[int, str] = Map(one_to_one=True)
        # Add each nutrient to the map
        for nutrient_id, nutrient_data in nutrients.items():
            nutrient_name_id_map.add_mapping(key=nutrient_id, value=nutrient_data["nutrient_name"])
        return nutrient_name_id_map

    def build_recipe_tag_name_id_map(self) -> Map[int, str]:
        """Fetches a bidirectional map of recipe tag names to IDs.
        Returns:
            Map: A bidirectional map of recipe tag names to IDs.
        """
        # Fetch all the recipe tags
        recipe_tags = self.repository.read_all_global_recipe_tags()
        # Create a bidirectional map
        recipe_tag_name_id_map: Map[int, str] = Map(one_to_one=True)
        # Add each recipe tag to the map
        for tag_id, tag_name in recipe_tags.items():
            recipe_tag_name_id_map.add_mapping(key=tag_id, value=tag_name)
        return recipe_tag_name_id_map

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

    def read_all_global_mass_units(self) -> dict[int, Unit]:
        """Returns all the global mass units.
        Returns:
            dict[int, Unit]: A dictionary of global mass units, where the key is the
            id of each specific mass unit.
        """
        # Read all the units
        all_units = self.read_all_global_units()
        # Filter out only the mass units
        mass_units = {unit_id: unit for unit_id, unit in all_units.items() if unit.type == "mass"}
        # Return
        return mass_units

    def read_all_global_unit_conversions(self) -> dict[int, UnitConversion]:
        """Returns all the global unit conversions.
        Returns:
            dict[int, UnitConversion]: A dictionary of global unit conversions, where the key is the
            id of each specific unit conversion.
        """
        # Fetch the raw data from the repo
        raw_conversion_data = self.repository.read_all_global_unit_conversions()
        # Init a dict to hold the unit conversions
        conversions = {}
        # Cycle through the raw data
        for conversion_id, conversion_data in raw_conversion_data.items():
            # Create a new unit conversion
            conversions[conversion_id] = UnitConversion(
                id=conversion_id,
                from_unit_id=conversion_data["from_unit_id"], # type: ignore
                to_unit_id=conversion_data["to_unit_id"], # type: ignore
                from_unit_qty=conversion_data["from_unit_qty"],
                to_unit_qty=conversion_data["to_unit_qty"],
            )
        return conversions

    def read_all_global_nutrients(self) -> dict[int, Nutrient]:
        """Returns all the global nutrients.
        Returns:
            Dict[int, Nutrient]: A dictionary of global nutrients, where the key is the
            id of each specific nutrient.
        """
        # Fetch the data for all the nutrients
        all_nutrients_data = self.repository.read_all_global_nutrients()
        
        # Init a dict to hold the nutrients and a dict to hold child relationships
        nutrients = {}
        children = {}
        
        # Cycle through the raw data to create nutrients and record child relationships
        for nutrient_id, nutrient_data in all_nutrients_data.items():
            nutrient = Nutrient(
                id=nutrient_id,
                nutrient_name=nutrient_data["nutrient_name"],
                aliases=nutrient_data["aliases"],
                parent_id=nutrient_data["parent_id"],
            )
            nutrients[nutrient_id] = nutrient
            if nutrient.parent_id is not None:
                if nutrient.parent_id not in children:
                    children[nutrient.parent_id] = []
                children[nutrient.parent_id].append(nutrient_id)
        
        # Populate the child_ids for each nutrient
        for nutrient_id, nutrient in nutrients.items():
            nutrient.child_ids = children.get(nutrient_id, [])
        
        return nutrients

    def read_ingredient(self, ingredient_id: int) -> Ingredient:
        """Returns the ingredient with the given name.
        Args:
            ingredient_id (int): The id of the ingredient.
        Returns:
            Ingredient: The ingredient with the given id.
        """
        # Fetch the ingredient name corresponding to the id
        ingredient_name = self.repository.read_ingredient_name(ingredient_id)
        # Fetch the ingredient standard id
        standard_unit_id = self.repository.read_ingredient_standard_unit_id(
            ingredient_id
        )
        # Init a fresh ingredient instance
        ingredient = Ingredient(
            id=ingredient_id,
            name=ingredient_name,
            standard_unit_id=standard_unit_id,
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
        # Fetch the unit conversions
        unit_conversions = self.read_ingredient_unit_conversions(
            ingredient_id=ingredient.id
        )
        for _, conversion in unit_conversions.items():
            ingredient.add_unit_conversion(conversion)
        # Fetch the flags
        flags = self.repository.read_ingredient_flags(ingredient.id)
        for flag_id, flag_value in flags.items():
            ingredient.add_flag(flag_id, flag_value)
        # Fetch the GI
        ingredient.gi = self.repository.read_ingredient_gi(ingredient.id)
        # Fetch the nutrients
        nutrient_quantities = self.read_ingredient_nutrient_quantities(
            ingredient_id=ingredient.id
        )
        for _, nutrient_quantity in nutrient_quantities.items():
            ingredient.add_nutrient_quantity(nutrient_quantity)
        # Return the completed ingredient
        return ingredient

    def read_ingredient_unit_conversions(
        self, ingredient_id: int
    ) -> dict[int, EntityUnitConversion]:
        """Returns a list of unit conversions for the given ingredient.
        Args:
            ingredient_id (int): The id of the ingredient.
        Returns:
            dict[int, EntityUnitConversion]: A dictionary of unit conversions, where the key is the
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
            conversions[conversion_id] = EntityUnitConversion(
                entity_id=ingredient_id,
                id=conversion_id,
                from_unit_id=conversion_data["from_unit_id"],
                from_unit_qty=conversion_data["from_unit_qty"],
                to_unit_id=conversion_data["to_unit_id"],
                to_unit_qty=conversion_data["to_unit_qty"],
            )
        return conversions

    def read_ingredient_nutrient_quantities(
        self, ingredient_id: int
    ) -> dict[int, EntityNutrientQuantity]:
        """Returns the nutrient quantities for the given ingredient.
        Args:
            ingredient_id (int): The id of the ingredient.
        Returns:
            dict[int, IngredientNutrientQuantity]: A dictionary of nutrient quantities, where the key is the
            id of each specific nutrient quantity.
        """
        # Init a dict to hold the nutrient quantities
        nutrient_quantities: dict[int, EntityNutrientQuantity] = {}
        # Fetch the raw data from the repo
        raw_nutrient_quantities = self._repo.read_ingredient_nutrient_quantities(
            ingredient_id
        )
        # Cycle through the raw data
        for nutrient_id, nutrient_qty_data in raw_nutrient_quantities.items():
            # And add the data to the dict
            nutrient_quantities[nutrient_id] = EntityNutrientQuantity(
                id=nutrient_qty_data["id"],
                nutrient_id=nutrient_id,
                entity_id=ingredient_id,
                ntr_mass_value=nutrient_qty_data["ntr_mass_value"],
                ntr_mass_unit_id=nutrient_qty_data["ntr_mass_unit_id"],
                entity_grams_qty=nutrient_qty_data["ing_grams_value"],
            )
        return nutrient_quantities

    def read_recipe(self, recipe_id: int) -> Recipe:
        """Returns the name of the recipe with the given ID."""
        raise NotImplementedError

    def update_ingredient(self, ingredient: Ingredient) -> None:
        """Updates the ingredient in the database."""
        # To use update, id must be set
        if ingredient.id is None:
            raise ValueError("Ingredient ID must be set.")
        # Update the name
        self.update_ingredient_name(ingredient.id, ingredient.name) # type: ignore
        # Update the description
        self.repository.update_ingredient_description(
            ingredient.id, ingredient.description
        )
        # Update the standard unit
        self.repository.update_ingredient_standard_unit_id(
            ingredient.id, ingredient.standard_unit_id
        )
        # Update the unit conversions
        # Read the existing saved unit conversions
        existing_unit_conversions = self.repository.read_ingredient_unit_conversions(
            ingredient.id
        )
        # Compare the existing unit conversions with the new ones
        for unit_conversion in ingredient.unit_conversions.values():
            # If the unit conversion is new, add it
            if unit_conversion.id not in existing_unit_conversions:
                self.repository.create_ingredient_unit_conversion(
                    ingredient_id=ingredient.id,
                    from_unit_id=unit_conversion.from_unit_id,
                    from_unit_qty=unit_conversion.from_unit_qty,
                    to_unit_id=unit_conversion.to_unit_id,
                    to_unit_qty=unit_conversion.to_unit_qty,
                )
            # If the unit conversion is already saved, update it
            else:
                self.repository.update_ingredient_unit_conversion(
                    ingredient_unit_id=unit_conversion.id,
                    from_unit_id=unit_conversion.from_unit_id,
                    from_unit_qty=unit_conversion.from_unit_qty,
                    to_unit_id=unit_conversion.to_unit_id,
                    to_unit_qty=unit_conversion.to_unit_qty,
                )
        # Delete any unit conversions that are no longer needed
        for unit_conversion_id in existing_unit_conversions.keys():
            if unit_conversion_id not in ingredient.unit_conversions:
                self.repository.delete_ingredient_unit_conversion(unit_conversion_id)      
        # Update the cost data
        self.repository.update_ingredient_cost(
            ingredient_id=ingredient.id,
            cost_value=ingredient.cost_value,
            cost_qty_unit_id=ingredient.cost_qty_unit_id,
            cost_qty_value=ingredient.cost_qty_value,
        )
        # Update the flags
        # Read the existing saved flags
        existing_flags = self.repository.read_ingredient_flags(ingredient.id)
        # Compare the existing flags with the new ones
        for flag_id, flag_value in ingredient.flags.items():
            # If the flag is new, add it
            if flag_id not in existing_flags:
                self.repository.create_ingredient_flag(
                    ingredient_id=ingredient.id,
                    flag_id=flag_id,
                    flag_value=flag_value,
                )
            # If the flag is already saved, update it
            else:
                self.repository.update_ingredient_flag(
                    ingredient_id=ingredient.id,
                    flag_id=flag_id,
                    flag_value=flag_value,
                )
        # Delete any flags that are no longer needed
        for flag_id in existing_flags.keys():
            if flag_id not in ingredient.flags:
                self.repository.delete_ingredient_flag(ingredient.id, flag_id)
        # Update the GI
        self.repository.update_ingredient_gi(ingredient.id, ingredient.gi)
        # Update the nutrient quantities
        # First, read the existing saved nutrient quantities
        existing_nutrient_quantities = self.repository.read_ingredient_nutrient_quantities(
            ingredient.id
        )
        # Compare the existing nutrient quantities with the new ones
        for nutrient_quantity in ingredient.nutrient_quantities.values():
            # If the nutrient quantity is new, add it
            if nutrient_quantity.id not in existing_nutrient_quantities:
                self.repository.create_ingredient_nutrient_quantity(
                    ingredient_id=ingredient.id,
                    global_nutrient_id=nutrient_quantity.nutrient_id,
                    ntr_mass_qty=nutrient_quantity.nutrient_mass_value,
                    ntr_mass_unit_id=nutrient_quantity.nutrient_mass_unit_id,
                    ing_grams_qty=nutrient_quantity.entity_grams_value,
                )
            # If the nutrient quantity is already saved, update it
            else:
                self.repository.update_ingredient_nutrient_quantity(
                    ingredient_id=ingredient.id,
                    global_nutrient_id=nutrient_quantity.nutrient_id,
                    ntr_mass_qty=nutrient_quantity.nutrient_mass_value,
                    ntr_mass_unit_id=nutrient_quantity.nutrient_mass_unit_id,
                    ing_grams_qty=nutrient_quantity.entity_grams_value,
                )
        # Delete any nutrient quantities that are no longer needed
        for nutrient_quantity_id in existing_nutrient_quantities.keys():
            if nutrient_quantity_id not in ingredient.nutrient_quantities:
                self.repository.delete_ingredient_nutrient_quantity(
                    ingredient_id=ingredient.id, global_nutrient_id=nutrient_quantity_id
                )

    def update_ingredient_name(self, ingredient_id: int, new_name: str) -> None:
        """Updates the name of the ingredient in the database.
        Args:
            ingredient_id (int): The id of the ingredient.
            new_name (str): The new name of the ingredient.
        """
        if new_name is None:
            raise ValueError("Ingredient name must be set.")
        self.repository.update_ingredient_name(ingredient_id, new_name)

    def update_ingredient_unit_conversion(self, unit_conversion: EntityUnitConversion) -> None:
        """Updates the unit conversion in the database."""
        self.repository.update_ingredient_unit_conversion(
            ingredient_unit_id=unit_conversion.id,
            from_unit_id=unit_conversion.from_unit_id,
            from_unit_qty=unit_conversion.from_unit_qty,
            to_unit_id=unit_conversion.to_unit_id,
            to_unit_qty=unit_conversion.to_unit_qty,
        )

    def update_ingredient_nutrient_quantity(self, ing_nutr_qty: EntityNutrientQuantity) -> None:
        """Updates the nutrient quantity in the database.
        Args:
            ing_nutr_qty (EntityNutrientQuantity): The nutrient quantity object.
        """
        # Raise an exception if the parent entity ID is not set
        if ing_nutr_qty.parent_entity_id is None:
            raise ValueError("The parent entity ID must be set.")
        # Update the nutrient quantity in the database
        self.repository.update_ingredient_nutrient_quantity(
            ingredient_id=ing_nutr_qty.parent_entity_id,
            global_nutrient_id=ing_nutr_qty.nutrient_id,
            ntr_mass_qty=ing_nutr_qty.nutrient_mass_value,
            ntr_mass_unit_id=ing_nutr_qty.nutrient_mass_unit_id,
            ing_grams_qty=ing_nutr_qty.entity_grams_value,
        )

    def delete_ingredient_unit_conversions(self, ingredient_id: int) -> None:
        """Deletes all the unit conversions for the given ingredient.
        Args:
            ingredient_id (int): The id of the ingredient.
        """
        # Read all of the unit conversions
        unit_conversions = self.repository.read_ingredient_unit_conversions(ingredient_id)
        # Delete each unit conversion
        for id in unit_conversions.keys():
            self.repository.delete_ingredient_unit_conversion(id)