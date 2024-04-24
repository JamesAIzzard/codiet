from codiet.models.ingredient import Ingredient
from codiet.models.recipe import Recipe
from codiet.models.nutrients import create_nutrient_dict
from codiet.db.repository import Repository
from codiet.utils.search import filter_text
from codiet.db import DB_PATH
from codiet.db.database import Database
from codiet.db.repository import Repository

class DatabaseService:
    def __init__(self):
        # Init the database
        self._repo = Repository(Database(DB_PATH))

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._repo._db.connection.close()

    def insert_global_flag(self, flag_name:str):
        """Inserts a global flag into the database."""
        self._repo.insert_global_flag(flag_name)

    def fetch_all_global_flag_names(self) -> list[str]:
        """Returns a list of all the flags in the database."""
        return self._repo.fetch_all_global_flag_names()
    
    def fetch_all_leaf_nutrient_names(self) -> list[str]:
        """Returns a list of all the leaf nutrients in the database."""
        return self._repo.fetch_all_leaf_nutrient_names()

    def fetch_all_group_nutrient_names(self) -> list[str]:
        """Returns a list of all the group nutrients in the database."""
        return self._repo.fetch_all_group_nutrient_names()

    def insert_global_group_nutrient(self, nutrient_name:str, parent_id: int | None = None) -> int:
        """Inserts a global group nutrient into the database."""
        return self._repo.insert_global_group_nutrient(nutrient_name, parent_id)

    def insert_global_leaf_nutrient(self, nutrient_name:str, parent_id: int | None = None) -> int:
        """Inserts a global leaf nutrient into the database."""
        return self._repo.insert_global_leaf_nutrient(nutrient_name, parent_id)

    def fetch_matching_ingredient_names(self, name: str) -> list[str]:
        """Returns a list of ingredient names that match the given name."""
        all_names = self._repo.fetch_all_ingredient_names()
        return filter_text(name, all_names, 10)

    def create_empty_ingredient(self) -> Ingredient:
        """Creates an ingredient."""
        # Init the ingredient
        ingredient = Ingredient()

        # Populate the flag dict
        flags = self._repo.fetch_all_global_flag_names()
        for flag in flags:
            ingredient._flags[flag] = False

        # Populate the nutrient dict
        nutrients = self._repo.fetch_all_leaf_nutrient_names()
        for nutrient in nutrients:
            ingredient.nutrients[nutrient] = create_nutrient_dict()

        return ingredient    

    def insert_new_ingredient(self, ingredient: Ingredient) -> int:
        """Saves the given ingredient to the database."""

        # If the ingredient name is not set on the ingredient, raise an exception
        if ingredient.name is None:
            raise ValueError("Ingredient name must be set.")
        
        try:
            # Add the ingredient name to the database, getting primary key
            self._repo.insert_ingredient_name(ingredient.name)

            # Get the ingredient ID from the database
            ingredient_id = self._repo.fetch_ingredient_id(ingredient.name)

            # Update the ingredient description
            self._repo.update_ingredient_description(
                ingredient_id=ingredient_id,
                description=ingredient.description,
            )

            # Add the ingredient cost data
            self._repo.update_ingredient_cost(
                ingredient_id=ingredient_id,
                cost_value=ingredient.cost_value,
                cost_unit=ingredient.cost_unit,
                qty_unit=ingredient.cost_qty_unit,
                qty_value=ingredient.cost_qty_value,
            )

            # Add the ingredient density data
            self._repo.update_ingredient_density(
                ingredient_id=ingredient_id,
                dens_mass_unit=ingredient.density_mass_unit,
                dens_mass_value=ingredient.density_mass_value,
                dens_vol_unit=ingredient.density_vol_unit,
                dens_vol_value=ingredient.density_vol_value,
            )

            # Add the ingredient piece mass data
            self._repo.update_ingredient_pc_mass(
                ingredient_id=ingredient_id,
                pc_qty=ingredient.pc_qty,
                pc_mass_unit=ingredient.pc_mass_unit,
                pc_mass_value=ingredient.pc_mass_value,
            )

            # Add the flags
            self._repo.update_ingredient_flags(ingredient_id, ingredient.flags)

            # Add the ingredient GI
            self._repo.update_ingredient_gi(ingredient_id, ingredient.gi)

            # Add the nutrients
            self._repo.update_ingredient_nutrients(ingredient_id, ingredient.nutrients)

            # Commit the transaction
            self._repo._db.connection.commit()

            # Return the ingredient ID
            return ingredient_id

        except Exception as e:
            # Roll back the transaction if an exception occurs
            self._repo._db.connection.rollback()
            # Re-raise any exceptions
            raise e

    def fetch_ingredient(self, name: str) -> Ingredient:
        """Returns the ingredient with the given name."""    
        # Init a fresh ingredient instance
        ingredient = self.create_empty_ingredient()

        # Grab the ID of the ingredient
        ingredient.id = self._repo.fetch_ingredient_id(name)  

        # Set the name
        ingredient.name = name

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
        ingredient.set_flags(self._repo.fetch_ingredient_flags(ingredient.id))

        # Fetch the GI
        ingredient.gi = self._repo.fetch_ingredient_gi(ingredient.id)

        # Fetch the nutrients
        ingredient.nutrients = self._repo.fetch_ingredient_nutrients(ingredient.id)

        return ingredient


    def fetch_ingredient_name(self, id:int) -> str:
        """Returns the name of the ingredient with the given ID."""
        return self._repo.fetch_ingredient_name(id)

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
            self._repo.update_ingredient_nutrients(ingredient.id, ingredient.nutrients)

            # Commit the transaction
            self._repo._db.connection.commit()

        except Exception as e:
            # Roll back the transaction if an exception occurs
            self._repo._db.connection.rollback()
            # Re-raise any exceptions
            raise e

    def delete_ingredient(self, ingredient_name:str):
        """Deletes the given ingredient from the database."""
        self._repo.delete_ingredient(ingredient_name)

    def create_empty_recipe(self) -> Recipe:
        """Creates an empty recipe."""
        # Init the recipe
        recipe = Recipe()

        return recipe
    
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
            self._repo.update_recipe_ingredients(
                recipe_id=recipe.id,
                ingredients=recipe.ingredients,
            )
            # Update the recipe serve times
            self._repo.update_recipe_serve_times(
                recipe_id=recipe.id,
                serve_times=recipe.serve_times_strings,
            )
            # Update the recipe types
            self._repo.update_recipe_types(
                recipe_id=recipe.id,
                recipe_types=recipe.recipe_types,
            )
            # Commit the transaction
            self._repo._db.connection.commit()
        except Exception as e:
            # Roll back the transaction if an exception occurs
            self._repo._db.connection.rollback()
            # Re-raise any exceptions
            raise e
        
    def fetch_recipe_name(self, id:int) -> str:
        """Returns the name of the recipe with the given ID."""
        return self._repo.fetch_recipe_name(id)
    
    def insert_global_recipe_type(self, recipe_type_name:str) -> int:
        """Inserts a global recipe type into the database."""
        # Action the insertion
        id = self._repo.insert_global_recipe_type(recipe_type_name)
        # Commit the transaction
        self._repo._db.connection.commit()
        # Return the ID
        return id