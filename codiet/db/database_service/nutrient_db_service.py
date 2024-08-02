from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from . import DatabaseService
from ..repository import Repository
from codiet.utils.map import Map

class NutrientDBService(QObject):
    """Database service module for nutrients."""

    ingredientNutrientsChanged = pyqtSignal()

    def __init__(self, repository: Repository, db_service: 'DatabaseService'):
        """Initialise the nutrient database service."""
        super().__init__()

        self.repository = repository
        self.db_service = db_service

        # Cache the global nutrient id-name map
        self._global_nutrient_id_name_map:Map[int, str]|None = None