from codiet.db.repository import Repository
from .unit_db_service import UnitDBService
from .flag_db_service import FlagDBService
from .nutrient_db_service import NutrientDBService
from .recipe_db_service import RecipeDBService
from .ingredient_db_service import IngredientDBService

class DatabaseService:
    """Service for interacting with the database."""

    def __init__(self, repository: Repository, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._repo = repository

        # Initialise sub-services
        self.units = UnitDBService(db_service=self, repository=self._repo)
        self.flags = FlagDBService(db_service=self, repository=self._repo)
        self.nutrients = NutrientDBService(db_service=self, repository=self._repo)
        self.recipes = RecipeDBService(db_service=self, repository=self._repo)
        self.ingredients = IngredientDBService(db_service=self, repository=self._repo)        

    @property
    def repository(self) -> Repository:
        return self._repo