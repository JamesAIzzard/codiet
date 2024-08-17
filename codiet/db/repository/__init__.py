from codiet.db.database import Database
from .unit_repository import UnitRepository
from .flag_repository import FlagRepository
from .nutrient_repository import NutrientRepository
from .ingredient_repository import IngredientRepository

class Repository:

    def __init__(self, database: Database):

        self._database = database

        # Create a submodule for each main section of the model
        self.units = UnitRepository(database=database)
        self.flags = FlagRepository(database=self._database)
        self.nutrients = NutrientRepository(database=self._database)
        # self.time = TimeRepository(database=self._database)
        self.ingredients = IngredientRepository(database=self._database)        
        # self.recipes = RecipeRepository(database=self._database)        

    def close_connection(self) -> None:
        """Close the connection to the database."""
        self._database.connection.close()