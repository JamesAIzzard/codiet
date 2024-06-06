from codiet.utils.time import (
    convert_datetime_interval_to_time_string_interval,
    convert_time_string_interval_to_datetime_interval,
)
from codiet.models.ingredients import (
    Ingredient,
    IngredientNutrientQuantity,
    IngredientQuantity,
)
from codiet.models.units import CustomUnit
from codiet.models.recipes import Recipe
from codiet.db.repository import Repository
from codiet.db import DB_PATH
from codiet.db.database import Database
from codiet.db.repository import Repository


class DatabaseService:
    """Service for interacting with the database."""

    def __init__(self):
        # Init the database
        self._repo = Repository(Database(DB_PATH))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Rollback any unsaved changes
        self._repo._db.connection.rollback()
        # Close the connection
        self._repo._db.connection.close()

    def create_empty_ingredient(self) -> Ingredient:
        """Creates an ingredient."""
        # Init the ingredient
        ingredient = Ingredient()

        # Populate the flag dict
        flags = self._repo.fetch_all_global_flag_names()
        for flag in flags:
            ingredient._flags[flag] = False

        # Populate the nutrient dict
        # Grab all the leaf nutrients
        nutrients = self._repo.fetch_all_leaf_nutrient_names()
        # Cycle through them, and create a nutrient quantity for each
        # and add it to the ingredient's nutrient dict
        for nutrient in nutrients:
            ingredient._nutrients[nutrient] = IngredientNutrientQuantity(nutrient)

        # Return the ingredient
        return ingredient

    def insert_global_flag(self, flag_name: str):
        """Inserts a global flag into the database."""
        self._repo.insert_global_flag(flag_name)

    def insert_global_flags(self, flags: list[str]):
        """Inserts a list of global flags into the database."""
        for flag in flags:
            self.insert_global_flag(flag)

    def insert_new_ingredient(self, ingredient: Ingredient) -> int:
        """Saves the given ingredient to the database."""
        # If the ingredient name is not set on the ingredient, raise an exception
        if ingredient.name is None:
            raise ValueError("Ingredient name must be set.")
        try:
            # Add the ingredient name to the database, getting primary key
            self._repo.insert_ingredient_name(ingredient.name)
            # Get the ingredient ID from the database and set it on the ingredient
            ingredient.id = self._repo.fetch_ingredient_id_by_name(ingredient.name)
            # Now we can use the update method, becuase the ID is set.
            self.update_ingredient(ingredient)
            # Return the ID
            return ingredient.id
        except Exception as e:
            # Roll back the transaction if an exception occurs
            self._repo._db.connection.rollback()
            # Re-raise any exceptions
            raise e

    def insert_custom_measurement(self, ingredient_id: int, measurement:CustomUnit) -> int:
        """Inserts a custom measurement into the database and returns the new ID."""
        return self._repo.insert_custom_measurement(
            ingredient_id=ingredient_id,
            unit_name=measurement.unit_name,
            custom_unit_qty=measurement.custom_unit_qty,
            std_unit_name=measurement.std_unit_name,
            std_unit_qty=measurement.std_unit_qty,
        )

    def insert_new_recipe(self, recipe: Recipe) -> None:
        """Saves the given recipe to the database."""
        # Check the recipe name is set, otherwise raise an exception
        if recipe.name is None:
            raise ValueError("Recipe name must be set.")
        try:
            # Add the recipe name to the database, getting primary key
            id = self._repo.insert_recipe_name(recipe.name)
            # Add the id to the recipe instance
            recipe.id = id
            # Now update the recipe as normal
            self.update_recipe(recipe)
        except Exception as e:
            # Roll back the transaction if an exception occurs
            self._repo._db.connection.rollback()
            # Re-raise any exceptions
            raise e

    def insert_global_recipe_tag(self, recipe_tag_name: str) -> int:
        """Inserts a global recipe tag into the database."""
        # Action the insertion
        id = self._repo.insert_global_recipe_tag(recipe_tag_name)
        # Return the ID
        return id

    def insert_global_leaf_nutrient(
        self, nutrient_name: str, parent_id: int | None = None
    ) -> int:
        """Inserts a global leaf nutrient into the database."""
        return self._repo.insert_global_leaf_nutrient(nutrient_name, parent_id)

    def fetch_all_global_flag_names(self) -> list[str]:
        """Returns a list of all the flags in the database."""
        return self._repo.fetch_all_global_flag_names()

    def fetch_all_leaf_nutrient_names(self) -> list[str]:
        """Returns a list of all the leaf nutrients in the database."""
        return self._repo.fetch_all_leaf_nutrient_names()

    def fetch_all_group_nutrient_names(self) -> list[str]:
        """Returns a list of all the group nutrients in the database."""
        return self._repo.fetch_all_group_nutrient_names()

    def insert_global_group_nutrient(
        self, nutrient_name: str, parent_id: int | None = None
    ) -> int:
        """Inserts a global group nutrient into the database."""
        return self._repo.insert_global_group_nutrient(nutrient_name, parent_id)

    def fetch_all_ingredient_names(self) -> list[str]:
        """Returns a list of all the ingredients in the database."""
        return self._repo.fetch_all_ingredient_names()

    def fetch_ingredient_by_name(self, name: str) -> Ingredient:
        """Returns the ingredient with the given name."""
        # Init a fresh ingredient instance
        ingredient = self.create_empty_ingredient()
        # Set the name
        ingredient.name = name
        # Set the ID
        ingredient.id = self._repo.fetch_ingredient_id_by_name(name)
        # Fetch the description
        ingredient.description = self._repo.fetch_ingredient_description(ingredient.id)
        # Fetch the cost data
        cost_data = self._repo.fetch_ingredient_cost(ingredient.id)
        ingredient.cost_value = cost_data[0]
        ingredient.cost_qty_unit = cost_data[1]
        ingredient.cost_qty_value = cost_data[2]
        # TODO: Fetch the custom measurements
        # Fetch the flags
        ingredient.set_flags(self.fetch_ingredient_flags(ingredient_id=ingredient.id))
        # Fetch the GI
        ingredient.gi = self._repo.fetch_ingredient_gi(ingredient.id)
        # Fetch the nutrients
        nutrient_data = self._repo.fetch_ingredient_nutrients(ingredient.id)
        for name, data in nutrient_data.items():
            # Create a new nutrient quantity
            nutrient_quantity = IngredientNutrientQuantity(
                nutrient_name=name,
                ntr_mass_value=data["ntr_qty_value"],
                ntr_mass_unit=data["ntr_qty_unit"],
                ing_qty_value=data["ing_qty_value"],
                ing_qty_unit=data["ing_qty_unit"],
            )
            # Add to the ingredient
            ingredient.update_nutrient_quantity(nutrient_quantity)
        # Return the completed ingredient
        return ingredient

    def fetch_ingredient_by_id(self, id: int) -> Ingredient:
        """Returns the ingredient with the given ID."""
        # Grab the name corresponding to the id
        name = self._repo.fetch_ingredient_name(id)
        # Return the ingredient with the name
        return self.fetch_ingredient_by_name(name)

    def fetch_ingredient_name_by_id(self, id: int) -> str:
        """Returns the name of the ingredient with the given ID."""
        return self._repo.fetch_ingredient_name(id)

    def fetch_ingredient_id_by_name(self, name: str) -> int:
        """Returns the ID of the ingredient with the given name."""
        return self._repo.fetch_ingredient_id_by_name(name)

    def fetch_custom_measurements_by_ingredient_id(self, ingredient_id: int) -> list[CustomUnit]:
        """Returns a list of custom measurements for the given ingredient."""
        # Init a list to hold the custom measurements
        custom_measurements = []
        # Fetch the raw data from the repo
        raw_custom_measurements = self._repo.fetch_custom_measurements_by_ingredient_id(
            ingredient_id
        )
        # Cycle through the raw data
        for data in raw_custom_measurements:
            # Create a new custom measurement
            custom_measurement = CustomUnit(
                unit_name=data[0],
                custom_unit_qty=data[1],
                std_unit_qty=data[2],
                std_unit_name=data[3],
                unit_id=data[4],
            )
            # Add it to the list
            custom_measurements.append(custom_measurement)
        return custom_measurements

    def fetch_ingredient_flags(
        self, ingredient_name: str | None = None, ingredient_id: int | None = None
    ) -> dict[str, bool]:
        """Returns the flags for the given ingredient."""
        # Check one of the parameters is set
        if ingredient_name is None and ingredient_id is None:
            raise ValueError("Either ingredient_name or ingredient_id must be set.")
        # Grab the flags using the id
        if ingredient_id is None and ingredient_name is not None:
            id = self._repo.fetch_ingredient_id_by_name(ingredient_name)
        elif ingredient_id is not None:
            id = ingredient_id
        # Grab the flags
        flags_data = self._repo.fetch_ingredient_flags(id)
        # Convert the flags from binary to boolean
        flags = {}
        for flag_name, flag_value in flags_data.items():
            flags[flag_name] = bool(flag_value)
        return flags

    def fetch_recipe_name_using_id(self, id: int) -> str:
        """Returns the name of the recipe with the given ID."""
        return self._repo.fetch_recipe_name(id)

    def fetch_all_recipe_names(self) -> list[str]:
        """Returns a list of all the recipes in the database."""
        return self._repo.fetch_all_recipe_names()

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
        raw_ingredients = self._repo.fetch_recipe_ingredients(recipe.id)
        # Init a list to hold the ingredient quantities
        ingredient_quantities: dict[int, IngredientQuantity] = {}
        # Cycle through the raw data
        for ingredient_id, data in raw_ingredients.items():
            # Grab the ingredient
            ingredient = self.fetch_ingredient_by_id(ingredient_id)
            # Create a new ingredient quantity
            ingredient_quantity = IngredientQuantity(
                ingredient=ingredient,
                qty_value=data['qty_value'],
                qty_unit=data['qty_unit'],
                qty_utol=data['qty_utol'],
                qty_ltol=data['qty_ltol'],
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

    def update_ingredient(self, ingredient: Ingredient):
        """Updates the given ingredient in the database."""
        # If the ingredient ID is not present, raise an exception
        if ingredient.id is None:
            raise ValueError("Ingredient ID must be set.")
        # An ingredient cannot be edited to not have a name,
        # so if the name is not set, raise an exception
        if ingredient.name is None:
            raise ValueError("Ingredient name must be set.")
        try:
            # Update the ingredient name
            self._repo.update_ingredient_name(
                ingredient_id=ingredient.id,
                name=ingredient.name,
            )
            # Update the ingredient description
            self._repo.update_ingredient_description(
                ingredient_id=ingredient.id,
                description=ingredient.description,
            )
            # Update the ingredient cost data
            self._repo.update_ingredient_cost(
                ingredient_id=ingredient.id,
                cost_value=ingredient.cost_value,
                cost_unit=ingredient.cost_unit,
                qty_unit=ingredient.cost_qty_unit,
                qty_value=ingredient.cost_qty_value,
            )
            # Update the custom measurements
            for custom_measurement in ingredient.custom_units.values():
                if custom_measurement.unit_id is None:
                    self.insert_custom_measurement(ingredient.id, custom_measurement)
                else:
                    self.update_custom_measurement(custom_measurement)
            # Update the flags
            self._repo.update_ingredient_flags(ingredient.id, ingredient.flags)
            # Update the ingredient GI
            self._repo.update_ingredient_gi(ingredient.id, ingredient.gi)
            # Update each nutrient
            for nutrient_name, nutrient_qty in ingredient.nutrient_quantities.items():
                self.update_ingredient_nutrient_quantity(ingredient.id, nutrient_qty)

        except Exception as e:
            # Roll back the transaction if an exception occurs
            self._repo._db.connection.rollback()
            # Re-raise any exceptions
            raise e

    def update_custom_measurement(self, measurement: CustomUnit):
        """Updates the given custom measurement in the database."""
        # If the measurement ID is not set, raise an exception
        if measurement.unit_id is None:
            raise ValueError("Measurement ID must be set.")
        # If the measurement unit name is not set, raise an exception
        if measurement.unit_name is None:
            raise ValueError("Measurement unit name must be set.")
        try:
            self._repo.update_custom_measurement(
                measurement_id=measurement.unit_id,
                custom_unit_qty=measurement.custom_unit_qty,
                std_unit_qty=measurement.std_unit_qty,
                std_unit_name=measurement.std_unit_name,
            )
        except Exception as e:
            # Roll back the transaction if an exception occurs
            self._repo._db.connection.rollback()
            # Re-raise any exceptions
            raise e

    def update_ingredient_nutrient_quantity(
            self, 
            ingredient_id:int, 
            nutrient_quantity:IngredientNutrientQuantity
        ) -> None:
        """Updates a nutrient quantity on the ingredient."""
        self._repo.update_ingredient_nutrient_quantity(
            ingredient_id=ingredient_id,
            nutrient_name=nutrient_quantity.nutrient_name,
            ntr_qty_value=nutrient_quantity.nutrient_mass,
            ntr_qty_unit=nutrient_quantity.nutrient_mass_unit,
            ing_qty_value=nutrient_quantity.ingredient_quantity,
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
            for ingredient_name, ingredient_quantity in recipe.ingredient_quantities.items():
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
            self._repo._db.connection.rollback()
            # Re-raise any exceptions
            raise e

    def delete_ingredient_by_name(self, ingredient_name: str):
        """Deletes the given ingredient from the database."""
        self._repo.delete_ingredient_by_name(ingredient_name)

    def delete_custom_measurement(self, measurement_id: int):
        """Deletes the given custom measurement from the database."""
        self._repo.delete_custom_measurement(measurement_id)

    def delete_recipe_by_name(self, recipe_name: str):
        """Deletes the given recipe from the database."""
        self._repo.delete_recipe_by_name(recipe_name)

    def commit(self):
        """Commits the current transaction."""
        self._repo.connection.commit()
