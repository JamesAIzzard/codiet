from codiet.utils.time import (
    convert_datetime_interval_to_time_string_interval,
    convert_time_string_interval_to_datetime_interval,
)
from codiet.models.ingredients import (
    Ingredient,
    IngredientNutrientQuantity,
    IngredientQuantity,
)
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

    def create_empty_recipe(self) -> Recipe:
        """Creates an empty recipe."""
        # Init the recipe
        recipe = Recipe()

        return recipe

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

    def insert_global_recipe_type(self, recipe_type_name: str) -> int:
        """Inserts a global recipe type into the database."""
        # Action the insertion
        id = self._repo.insert_global_recipe_type(recipe_type_name)
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
        # Fetch the density data
        density_data = self._repo.fetch_ingredient_density(ingredient.id)
        ingredient.density_mass_unit = density_data[0]
        ingredient.density_mass_value = density_data[1]
        ingredient.density_vol_unit = density_data[2]
        ingredient.density_vol_value = density_data[3]
        # Fetch the piece mass data
        pc_mass_data = self._repo.fetch_ingredient_pc_mass(ingredient.id)
        ingredient.pc_qty = pc_mass_data[0]
        ingredient.pc_mass_unit = pc_mass_data[1]
        ingredient.pc_mass_value = pc_mass_data[2]
        # Fetch the flags
        ingredient.set_flags(self.fetch_ingredient_flags(ingredient_id=ingredient.id))
        # Fetch the GI
        ingredient.gi = self._repo.fetch_ingredient_gi(ingredient.id)
        # Fetch the nutrients
        nutrient_data = self._repo.fetch_ingredient_nutrients(ingredient.id)
        for name, data in nutrient_data.items():
            # Create a new nutrient quantity
            nutrient_quantity = IngredientNutrientQuantity(
                name=name,
                ntr_mass_value=data["ntr_qty_value"],
                ntr_mass_unit=data["ntr_qty_unit"],
                ing_qty_value=data["ing_qty_value"],
                ing_qty_unit=data["ing_qty_unit"],
            )
            # Add to the ingredient
            ingredient.update_nutrient_quantity(nutrient_quantity)
        # Return the completed ingredient
        return ingredient

    def fetch_ingredient_name_by_id(self, id: int) -> str:
        """Returns the name of the ingredient with the given ID."""
        return self._repo.fetch_ingredient_name(id)

    def fetch_ingredient_id_by_name(self, name: str) -> int:
        """Returns the ID of the ingredient with the given name."""
        return self._repo.fetch_ingredient_id_by_name(name)

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
        recipe = self.create_empty_recipe()
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
        ingredient_quantities: dict[str, IngredientQuantity] = {}
        # Cycle through the raw data
        for ingredient_name, data in raw_ingredients.items():
            # Grab the ingredient
            ingredient = self.fetch_ingredient_by_name(ingredient_name)
            # Create a new ingredient quantity
            ingredient_quantity = IngredientQuantity(
                ingredient=ingredient,
                qty_value=data[0],
                qty_unit=data[1],
                qty_utol=data[2],
                qty_ltol=data[3],
            )
            # Add it to the list
            ingredient_quantities[ingredient_name] = ingredient_quantity
        # Add the ingredient quanities list to the recipe
        recipe.ingredients = ingredient_quantities
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
        # Fetch the recipe types
        recipe.recipe_types = self._repo.fetch_recipe_types_for_recipe(recipe.id)

        return recipe

    def fetch_all_global_recipe_types(self) -> list[str]:
        """Returns a list of all the recipe types in the database."""
        return self._repo.fetch_all_global_recipe_types()

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
            # Update the ingredient density data
            self._repo.update_ingredient_density(
                ingredient_id=ingredient.id,
                dens_mass_unit=ingredient.density_mass_unit,
                dens_mass_value=ingredient.density_mass_value,
                dens_vol_unit=ingredient.density_vol_unit,
                dens_vol_value=ingredient.density_vol_value,
            )
            # Update the ingredient piece mass data
            self._repo.update_ingredient_pc_mass(
                ingredient_id=ingredient.id,
                pc_qty=ingredient.pc_qty,
                pc_mass_unit=ingredient.pc_mass_unit,
                pc_mass_value=ingredient.pc_mass_value,
            )
            # Update the flags
            self._repo.update_ingredient_flags(ingredient.id, ingredient.flags)
            # Update the ingredient GI
            self._repo.update_ingredient_gi(ingredient.id, ingredient.gi)
            # Update the nutrients
            # For a data dict for the nutrients
            nutr_data = {}
            for name, nutrient in ingredient.nutrient_quantities.items():
                nutr_data[name] = {
                    "ntr_qty_unit": nutrient.nutrient_mass_unit,
                    "ntr_qty_value": nutrient.nutrient_mass,
                    "ing_qty_unit": nutrient.ingredient_quantity_unit,
                    "ing_qty_value": nutrient.ingredient_quantity,
                }
            self._repo.update_ingredient_nutrients(ingredient.id, nutr_data)

        except Exception as e:
            # Roll back the transaction if an exception occurs
            self._repo._db.connection.rollback()
            # Re-raise any exceptions
            raise e

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
            for ingredient_name, ingredient_quantity in recipe.ingredients.items():
                ingredient_quantities[ingredient_name] = {
                    "qty": ingredient_quantity.qty_value,
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
            # Update the recipe types
            self._repo.update_recipe_types(
                recipe_id=recipe.id,
                recipe_types=recipe._recipe_types,
            )
        except Exception as e:
            # Roll back the transaction if an exception occurs
            self._repo._db.connection.rollback()
            # Re-raise any exceptions
            raise e

    def delete_ingredient(self, ingredient_name: str):
        """Deletes the given ingredient from the database."""
        self._repo.delete_ingredient(ingredient_name)

    def commit(self):
        """Commits the current transaction."""
        self._repo.connection.commit()
