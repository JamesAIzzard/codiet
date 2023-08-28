from codiet.models.ingredient import Ingredient
from codiet.db.repository import Repository

class DatabaseService:
    def __init__(self, repo: Repository):
        self.repo = repo

    def save_ingredient(self, ingredient: Ingredient):
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
                raise e