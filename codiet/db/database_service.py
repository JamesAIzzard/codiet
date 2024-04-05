from codiet.models.ingredient import Ingredient
from codiet.db.repository import Repository
from codiet.utils.search import filter_text
from codiet.db.repository import create_nutrient_dict

class DatabaseService:
    def __init__(self, repo: Repository):
        self.repo = repo

    def fetch_matching_ingredient_names(self, name: str) -> list[str]:
        """Returns a list of ingredient names that match the given name."""
        all_names = self.repo.fetch_all_ingredient_names()
        return filter_text(name, all_names, 10)

    def create_empty_ingredient(self) -> Ingredient:
        """Creates an ingredient."""
        # Init the ingredient
        ingredient = Ingredient()

        # Populate the flag dict
        flags = self.fetch_flag_names()
        for flag in flags:
            ingredient._flags[flag] = False

        # Populate the nutrient dict
        nutrients = self.repo.fetch_all_leaf_nutrient_names()
        for nutrient in nutrients:
            ingredient.nutrients[nutrient] = create_nutrient_dict()

        return ingredient    

    def create_ingredient(self, ingredient: Ingredient) -> int:
        """Saves the given ingredient to the database."""

        # If the ingredient name is not set on the ingredient, raise an exception
        if ingredient.name is None:
            raise ValueError("Ingredient name must be set.")
        
        with self.repo.db.connection:
            try:
                # Add the ingredient name to the database, getting primary key
                self.repo.insert_ingredient_entry(ingredient.name)

                # Get the ingredient ID from the database
                ingredient_id = self.repo.fetch_ingredient_id(ingredient.name)

                # Update the ingredient description
                self.repo.update_ingredient_description(
                    ingredient_id=ingredient_id,
                    description=ingredient.description,
                )

                # Add the ingredient cost data
                self.repo.update_ingredient_cost(
                    ingredient_id=ingredient_id,
                    cost_value=ingredient.cost_value,
                    qty_unit=ingredient.cost_qty_unit,
                    qty_value=ingredient.cost_qty_value,
                )

                # Add the ingredient density data
                self.repo.update_ingredient_density(
                    ingredient_id=ingredient_id,
                    dens_mass_unit=ingredient.density_mass_unit,
                    dens_mass_value=ingredient.density_mass_value,
                    dens_vol_unit=ingredient.density_vol_unit,
                    dens_vol_value=ingredient.density_vol_value,
                )

                # Add the ingredient piece mass data
                self.repo.update_ingredient_pc_mass(
                    ingredient_id=ingredient_id,
                    pc_qty=ingredient.pc_qty,
                    pc_mass_unit=ingredient.pc_mass_unit,
                    pc_mass_value=ingredient.pc_mass_value,
                )

                # Add the flags
                self.repo.update_ingredient_flags(ingredient_id, ingredient.flags)

                # Add the ingredient GI
                self.repo.update_ingredient_gi(ingredient_id, ingredient.gi)

                # Add the nutrients
                self.repo.update_ingredient_nutrients(ingredient_id, ingredient.nutrients)

                # Commit the transaction
                self.repo.db.connection.commit()

                # Return the ingredient ID
                return ingredient_id

            except Exception as e:
                # Roll back the transaction if an exception occurs
                self.repo.db.connection.rollback()
                # Re-raise any exceptions
                raise e

    def fetch_ingredient(self, name: str) -> Ingredient:
        """Returns the ingredient with the given name."""
        return self.repo.fetch_ingredient(name)

    def fetch_ingredient_name(self, id:int) -> str:
        """Returns the name of the ingredient with the given ID."""
        return self.repo.fetch_ingredient_name(id)

    def update_ingredient(self, ingredient: Ingredient):
        """Updates the given ingredient in the database."""
        # If the ingredient ID is not present, raise an exception
        if ingredient.id is None:
            raise ValueError("Ingredient ID must be set.")
        
        # An ingredient cannot be edited to not have a name,
        # so if the name is not set, raise an exception
        if ingredient.name is None:
            raise ValueError("Ingredient name must be set.")

        with self.repo.db.connection:
            try:
                # Update the ingredient name
                self.repo.update_ingredient_name(
                    ingredient_id=ingredient.id,
                    name=ingredient.name,
                )

                # Update the ingredient description
                self.repo.update_ingredient_description(
                    ingredient_id=ingredient.id,
                    description=ingredient.description,
                )

                # Update the ingredient cost data
                self.repo.update_ingredient_cost(
                    ingredient_id=ingredient.id,
                    cost_value=ingredient.cost_value,
                    qty_unit=ingredient.cost_qty_unit,
                    qty_value=ingredient.cost_qty_value,
                )

                # Update the ingredient density data
                self.repo.update_ingredient_density(
                    ingredient_id=ingredient.id,
                    dens_mass_unit=ingredient.density_mass_unit,
                    dens_mass_value=ingredient.density_mass_value,
                    dens_vol_unit=ingredient.density_vol_unit,
                    dens_vol_value=ingredient.density_vol_value,
                )

                # Update the ingredient piece mass data
                self.repo.update_ingredient_pc_mass(
                    ingredient_id=ingredient.id,
                    pc_qty=ingredient.pc_qty,
                    pc_mass_unit=ingredient.pc_mass_unit,
                    pc_mass_value=ingredient.pc_mass_value,
                )

                # Update the flags
                self.repo.update_ingredient_flags(ingredient.id, ingredient.flags)

                # Update the ingredient GI
                self.repo.update_ingredient_gi(ingredient.id, ingredient.gi)

                # Update the nutrients
                self.repo.update_ingredient_nutrients(ingredient.id, ingredient.nutrients)

                # Commit the transaction
                self.repo.db.connection.commit()

            except Exception as e:
                # Roll back the transaction if an exception occurs
                self.repo.db.connection.rollback()
                # Re-raise any exceptions
                raise e

    def delete_ingredient(self, ingredient_name:str):
        """Deletes the given ingredient from the database."""
        self.repo.delete_ingredient(ingredient_name)

    def fetch_flag_names(self) -> list[str]:
        """Returns a list of all the flags in the database."""
        return self.repo.fetch_all_flag_names()
    
    def get_all_nutrient_names(self):
        """Returns a list of all the nutrients in the database."""
        return self.repo.fetch_all_nutrient_names()
    
    def fetch_leaf_nutrient_names(self) -> list[str]:
        """Returns a list of all the leaf nutrients in the database."""
        return self.repo.fetch_all_leaf_nutrient_names()