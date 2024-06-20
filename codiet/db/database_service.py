from typing import Any

from codiet.db.repository import Repository
from codiet.utils.time import (
    convert_datetime_interval_to_time_string_interval,
    convert_time_string_interval_to_datetime_interval,
)
from codiet.utils.map import BidirectionalMap
from codiet.models.ingredients import (
    Ingredient,
    IngredientQuantity,
)
from codiet.models.nutrients import (
    Nutrient,
    IngredientNutrientQuantity,
)
from codiet.models.units import Unit
from codiet.models.recipes import Recipe

class DatabaseService:
    """Service for interacting with the database."""

    def __init__(self, repository: Repository):
        self._repo = repository

    @property
    def repository(self) -> Repository:
        return self._repo

    def create_global_flags(self, flags: list[str]) -> None:
        """Insert the global flags into the database."""
        for flag in flags:
            self.repository.insert_global_flag(flag)

    def create_global_nutrients(self, nutrient_data: dict[str, Any], parent_id: int|None=None) -> None:
        """Recursively adds nutrients and their aliases into the database."""
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

    def fetch_nutrient_id_name_map(self) -> BidirectionalMap:
        """Returns a bidirectional map of nutrient IDs to names."""
        # Create a new bidirectional map
        map = BidirectionalMap()
        # Fetch the raw data from the repo
        global_nutrients = self._repo.fetch_all_global_nutrients()
        for nutrient_id, nutrient_data in global_nutrients.items():
            map.add_mapping(integer=nutrient_id, string=nutrient_data['nutrient_name'])
        return map

    def fetch_ingredient(self, ingredient_id: int) -> Ingredient:
        """Returns the ingredient with the given name."""
        # Grab the ingredient ID
        id = self._repo.fetch_ingredient_id_by_name(name)
        # Init a fresh ingredient instance
        ingredient = self.create_empty_ingredient(
            ingredient_name=name,
            ingredient_id=id,
        )
        # Fetch the description
        ingredient.description = self._repo.fetch_ingredient_description(ingredient.id)
        # Fetch the cost data
        cost_data = self._repo.fetch_ingredient_cost(ingredient.id)
        ingredient.cost_value = cost_data[0]
        ingredient.cost_qty_unit = cost_data[1]
        ingredient.cost_qty_value = cost_data[2]
        # Fetch the custom units
        custom_units = self.fetch_custom_units_by_ingredient_id(ingredient.id)
        for custom_unit in custom_units.values():
            ingredient.add_custom_unit(custom_unit)
        # Fetch the flags
        ingredient.set_flags(self.fetch_ingredient_flags(ingredient_id=ingredient.id))
        # Fetch the GI
        ingredient.gi = self._repo.fetch_ingredient_gi(ingredient.id)
        # Fetch the nutrients
        nutrient_quantities = self.fetch_nutrient_quantities_by_ingredient_id(
            ingredient_id=ingredient.id
        )
        ingredient._nutrient_quantities = nutrient_quantities
        # Return the completed ingredient
        return ingredient

    def fetch_custom_units_by_ingredient_id(
        self, ingredient_id: int
    ) -> dict[int, Unit]:
        """Returns a list of custom units for the given ingredient."""
        # Init a list to hold the custom units
        custom_units = {}
        # Fetch the raw data from the repo
        raw_custom_units = self._repo.fetch_ingredient_units(ingredient_id)
        # Cycle through the raw data
        for data in raw_custom_units:
            # Create a new custom unit
            custom_unit = Unit(
                unit_name=data[0],
                custom_unit_qty=data[1],
                std_unit_qty=data[2],
                std_unit_name=data[3],
                global_unit_id=data[4],
            )
            # Add it to the list
            custom_units[custom_unit.unit_id] = custom_unit
        return custom_units

    def fetch_nutrient_quantities_by_ingredient_id(
        self, ingredient_id: int
    ) -> dict[int, IngredientNutrientQuantity]:
        """Returns the nutrient quantities for the given ingredient."""
        # Init a dict to hold the nutrient quantities
        nutrient_quantities = {}
        # Fetch the raw data from the repo
        raw_nutrient_quantities = self._repo.read_ingredient_nutrient_quantities(
            ingredient_id
        )
        # Cycle through the raw data
        for nutrient_id, nutrient_data in raw_nutrient_quantities.items():
            # Create a new nutrient quantity
            nutrient_quantity = IngredientNutrientQuantity(
                global_nutrient_id=nutrient_id,
                ingredient_id=ingredient_id,
                ntr_mass_value=nutrient_data[1],
                ntr_mass_unit=nutrient_data[0],
                ing_qty_value=nutrient_data[3],
                ing_qty_unit=nutrient_data[2],
            )
            # Add it to the list
            nutrient_quantities[nutrient_id] = (
                nutrient_quantity
            )
        return nutrient_quantities

    def fetch_recipe_name_using_id(self, id: int) -> str:
        """Returns the name of the recipe with the given ID."""
        return self._repo.fetch_recipe_name(id)

    def fetch_all_recipe_names(self) -> list[str]:
        """Returns a list of all the recipes in the database."""
        return self._repo.read_all_recipe_names()

    def fetch_recipe_by_name(self, name: str) -> Recipe:
        """Returns the recipe with the given name."""
        # Init a fresh recipe instance
        recipe = Recipe()
        # Grab the ID of the recipe
        recipe.id = self._repo.fetch_recipe_id(name)
        # Set the name
        recipe.name = name
        # Fetch the description
        recipe.description = self._repo.fetch_recipe_description(recipe.id)
        # Fetch the instructions
        recipe.instructions = self._repo.fetch_recipe_instructions(recipe.id)
        # Fetch the ingredients
        # First grab the raw data from the repo
        raw_ingredients = self._repo.read_recipe_ingredients(recipe.id)
        # Init a list to hold the ingredient quantities
        ingredient_quantities: dict[int, IngredientQuantity] = {}
        # Cycle through the raw data
        for ingredient_id, data in raw_ingredients.items():
            # Grab the ingredient
            ingredient = self.fetch_ingredient_by_id(ingredient_id)
            # Create a new ingredient quantity
            ingredient_quantity = IngredientQuantity(
                ingredient=ingredient,
                qty_value=data["qty_value"],
                qty_unit=data["qty_unit"],
                qty_utol=data["qty_utol"],
                qty_ltol=data["qty_ltol"],
            )
            # Add it to the list
            ingredient_quantities[ingredient_id] = ingredient_quantity
        # Add the ingredient quanities list to the recipe
        recipe.ingredient_quantities = ingredient_quantities
        # Fetch the serve times
        # First fetch the raw strings
        raw_serve_times = self._repo.fetch_recipe_serve_times(recipe.id)
        # Init a list to hold the serve times
        serve_times = []
        # Cycle through the raw strings
        for raw_serve_time in raw_serve_times:
            # Convert the string to a tuple of datetime objects
            serve_times.append(
                convert_time_string_interval_to_datetime_interval(raw_serve_time)
            )
        recipe.serve_times = serve_times
        # Fetch the recipe tags
        recipe.tags = self._repo.fetch_recipe_tags_for_recipe(recipe.id)

        return recipe

    def fetch_all_global_recipe_tags(self) -> list[str]:
        """Returns a list of all the recipe tags in the database."""
        return self._repo.fetch_all_global_recipe_tags()

    def update_ingredient_description(
        self, ingredient_id: int, description: str
    ) -> None:
        """Updates the description of the given ingredient."""
        self._repo.update_ingredient_description(ingredient_id, description)

    def update_ingredient_cost(
        self,
        ingredient_id: int,
        cost_unit: str = "GBP",
        cost_value: float | None = None,
        cost_qty_unit: str = "g",
        cost_qty_value: float | None = None,
    ) -> None:
        """Updates the cost value of the given ingredient."""
        self._repo.update_ingredient_cost(
            ingredient_id=ingredient_id,
            cost_value=cost_value,
            cost_unit=cost_unit,
            cost_qty_unit=cost_qty_unit,
            cost_qty_value=cost_qty_value,
        )

    def update_custom_unit(self, custom_unit: Unit):
        """Updates the given custom measurement in the database."""
        # If the measurement ID is not set, raise an exception
        if custom_unit.unit_id is None:
            raise ValueError("Measurement ID must be set.")
        # If the measurement unit name is not set, raise an exception
        if custom_unit.unit_name is None:
            raise ValueError("Measurement unit name must be set.")
        try:
            self._repo.update_custom_measurement(
                unit_id=custom_unit.unit_id,
                custom_unit_qty=custom_unit.custom_unit_qty,
                std_unit_qty=custom_unit.std_unit_qty,
                std_unit_name=custom_unit.std_unit_name,
            )
        except Exception as e:
            # Roll back the transaction if an exception occurs
            self._repo.database.connection.rollback()
            # Re-raise any exceptions
            raise e

    def update_ingredient_flag(
        self, ingredient_id: int, flag_name: str, flag_value: bool
    ) -> None:
        """Updates a flag on the ingredient."""
        self._repo.upsert_ingredient_flag(ingredient_id, flag_name, flag_value)

    def update_ingredient_gi(self, ingredient_id: int, gi_value: float | None) -> None:
        """Updates the GI value of the given ingredient."""
        self._repo.update_ingredient_gi(ingredient_id, gi_value)

    def update_ingredient_nutrient_quantity(
        self, nutrient_quantity: IngredientNutrientQuantity
    ) -> None:
        """Updates a nutrient quantity on the ingredient."""
        self._repo.upsert_ingredient_nutrient_quantity(
            ingredient_id=nutrient_quantity.ingredient_id,
            global_nutrient_id=nutrient_quantity.global_nutrient_id,
            ntr_mass_value=nutrient_quantity.nutrient_mass_value,
            ntr_mass_unit=nutrient_quantity.nutrient_mass_unit,
            ing_qty_value=nutrient_quantity.ingredient_quantity_value,
            ing_qty_unit=nutrient_quantity.ingredient_quantity_unit,
        )

    def update_recipe(self, recipe: Recipe):
        """Updates the given recipe in the database."""
        # Check the recipe ID is set, otherwise raise an exception
        if recipe.id is None:
            raise ValueError("Recipe ID must be set.")
        # Check the recipe name is set, otherwise raise an exception
        if recipe.name is None or recipe.name.strip() == "":
            raise ValueError("Recipe name must be set.")
        try:
            # Update the recipe name
            self._repo.update_recipe_name(
                recipe_id=recipe.id,
                name=recipe.name,
            )
            # Update the recipe description
            self._repo.update_recipe_description(
                recipe_id=recipe.id,
                description=recipe.description,
            )
            # Update the recipe instructions
            self._repo.update_recipe_instructions(
                recipe_id=recipe.id,
                instructions=recipe.instructions,
            )
            # Update the recipe ingredients
            # Form a dict to represent the ingredients
            ingredient_quantities = {}
            # For each ingredient in the recipe, add it to the dict
            for (
                ingredient_name,
                ingredient_quantity,
            ) in recipe.ingredient_quantities.items():
                ingredient_quantities[ingredient_name] = {
                    "qty_value": ingredient_quantity.qty_value,
                    "qty_unit": ingredient_quantity.qty_unit,
                    "qty_utol": ingredient_quantity.upper_tol,
                    "qty_ltol": ingredient_quantity.lower_tol,
                }
            # Submit this new dict to the repo method
            self._repo.update_recipe_ingredients(
                recipe_id=recipe.id,
                ingredients=ingredient_quantities,
            )
            # Update the recipe serve times
            # Need to convert the datetime objects to a list of strings
            serve_times = []
            for serve_time in recipe.serve_times:
                serve_times.append(
                    convert_datetime_interval_to_time_string_interval(serve_time)
                )
            # Submit the serve times to the repo method
            self._repo.update_recipe_serve_times(
                recipe_id=recipe.id,
                serve_times=serve_times,
            )
            # Update the recipe tags
            self._repo.update_recipe_tags(
                recipe_id=recipe.id,
                recipe_tags=recipe._recipe_tags,
            )
        except Exception as e:
            # Roll back the transaction if an exception occurs
            self._repo.database.connection.rollback()
            # Re-raise any exceptions
            raise e

    def delete_ingredient_by_name(self, ingredient_name: str):
        """Deletes the given ingredient from the database."""
        self._repo.delete_ingredient_by_name(ingredient_name)

    def delete_custom_unit(self, unit_id: int):
        """Deletes the given custom measurement from the database."""
        self._repo.delete_custom_unit(unit_id)

    def delete_recipe_by_name(self, recipe_name: str):
        """Deletes the given recipe from the database."""
        self._repo.delete_recipe_by_name(recipe_name)
