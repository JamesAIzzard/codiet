from codiet.models.ingredient import Ingredient
from codiet.db.repository import Repository
from codiet.utils.search import filter_text

class DatabaseService:
    def __init__(self, repo: Repository):
        self.repo = repo

    def load_matching_ingredient_names(self, name: str) -> list[str]:
        """Returns a list of ingredient names that match the given name."""
        all_names = self.repo.get_ingredient_names()
        return filter_text(name, all_names, 10)

    def save_ingredient(self, ingredient: Ingredient):
        """Saves the given ingredient to the database."""

        # If the ingredient name is not set on the ingredient, raise an exception
        if ingredient.name is None:
            raise ValueError("Ingredient name must be set.")
        
        with self.repo.db.connection:
            try:
                # Add the ingredient name to the database, getting primary key
                self.repo.add_ingredient_name(ingredient.name)

                # Get the ingredient ID from the database
                ingredient_id = self.repo.get_ingredient_id(ingredient.name)

                # Add the ingredient cost data
                self.repo.set_ingredient_cost(
                    ingredient_id=ingredient_id,
                    cost_unit=ingredient.cost_unit,
                    cost_value=ingredient.cost_value,
                    qty_unit=ingredient.cost_qty_unit,
                    qty_value=ingredient.cost_qty_value,
                )

                # Add the ingredient density data
                self.repo.set_ingredient_density(
                    ingredient_id=ingredient_id,
                    dens_mass_unit=ingredient.density_mass_unit,
                    dens_mass_value=ingredient.density_mass_value,
                    dens_vol_unit=ingredient.density_vol_unit,
                    dens_vol_value=ingredient.density_vol_value,
                )
            except Exception as e:
                # Roll back the transaction if an exception occurs
                self.repo.db.connection.rollback()
                # Re-raise any exceptions
                raise e

    def load_ingredient(self, name: str) -> Ingredient:
        """Returns the ingredient with the given name."""
        return self.repo.load_ingredient(name)

    def delete_ingredient(self, ingredient_name:str):
        """Deletes the given ingredient from the database."""
        self.repo.delete_ingredient(ingredient_name)

    def get_all_flags(self):
        """Returns a list of all the flags in the database."""
        return self.repo.get_all_flags()
    
    def get_all_nutrient_names(self):
        """Returns a list of all the nutrients in the database."""
        return self.repo.get_all_nutrient_names()