from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from . import DatabaseService
from codiet.db.repository import Repository
from codiet.utils.map import Map
from codiet.models.nutrients.nutrient import Nutrient
from codiet.models.nutrients.ingredient_nutrient_quantity import IngredientNutrientQuantity

class NutrientDBService(QObject):
    """Database service module for nutrients."""

    ingredientNutrientsChanged = pyqtSignal()

    def __init__(self, repository: Repository, db_service: 'DatabaseService'):
        """Initialise the nutrient database service."""
        super().__init__()

        self._repository = repository
        self._db_service = db_service

        # Cache the global nutrient id-name map
        self._global_nutrient_id_name_map:Map[int, str]|None = None

    @property
    def global_nutrient_id_name_map(self) -> Map[int, str]:
        """Get the global nutrient id-name map."""
        if self._global_nutrient_id_name_map is None:
            self._cache_global_nutrient_id_name_map()
        return self._global_nutrient_id_name_map # type: ignore # checked in the property setter

    def create_global_nutrients(self, nutrients:list[Nutrient]) -> dict[int, Nutrient]:
        """Create global nutrients in the database."""
        # Init a dict to store the created nutrients
        added_nutrients = {}

        # First, add each nutrient to the database
        for nutrient in nutrients:
            # Add the nutrient to the database
            id = self._repository.create_global_nutrient(
                name=nutrient.nutrient_name,
                parent_id=nutrient.parent_id,
            )

            # Update the ID
            nutrient.id = id

            # Add the aliases
            for alias in nutrient.aliases:
                self._repository.create_global_nutrient_alias(
                    primary_nutrient_id=id,
                    alias=alias,
                )   

            # Add the nutrient to the dict
            added_nutrients[id] = nutrient

        return added_nutrients

    def create_ingredient_nutrient_quantity(self, ing_nutr_qty: IngredientNutrientQuantity) -> IngredientNutrientQuantity:
        """Creates an entry for the ingredient nutrient quantity in the database.
        Returns the object, with the id populated.

        Args:
            ing_nutr_qty (EntityNutrientQuantity): The nutrient quantity object.
        Returns:
            EntityNutrientQuantity: The created nutrient quantity object.
        """
        # Raise an exception if the parent entity ID is not set
        if ing_nutr_qty.parent_entity_id is None:
            raise ValueError("The parent entity ID must be set.")
        
        # Insert the nutrient quantity into the database
        nutrient_quantity_id = self._repository.create_ingredient_nutrient_quantity(
            ingredient_id=ing_nutr_qty.parent_entity_id,
            global_nutrient_id=ing_nutr_qty.nutrient_id,
            ntr_mass_qty=ing_nutr_qty.nutrient_mass_value,
            ntr_mass_unit_id=ing_nutr_qty.nutrient_mass_unit_id,
            ing_grams_qty=ing_nutr_qty.entity_grams_value,
        )

        # Populate the ID
        ing_nutr_qty.id = nutrient_quantity_id

        # Emit the signal for the ingredient nutrients change
        self.ingredientNutrientsChanged.emit()

        return ing_nutr_qty
    
    def read_all_global_nutrients(self) -> dict[int, Nutrient]:
        """Returns all the global nutrients.
        Returns:
            Dict[int, Nutrient]: A dictionary of global nutrients, where the key is the
            id of each specific nutrient.
        """
        # Fetch the data for all the nutrients
        all_nutrients_data = self._repository.read_all_global_nutrients()
        
        # Init a dict to hold the nutrients and a dict to hold child relationships
        nutrients = {}
        children = {}
        
        # Cycle through the raw data to create nutrients and record child relationships
        for nutrient_id, nutrient_data in all_nutrients_data.items():
            nutrient = Nutrient(
                id=nutrient_id,
                nutrient_name=nutrient_data["nutrient_name"],
                aliases=nutrient_data["aliases"],
                parent_id=nutrient_data["parent_id"],
            )
            nutrients[nutrient_id] = nutrient
            if nutrient.parent_id is not None:
                if nutrient.parent_id not in children:
                    children[nutrient.parent_id] = []
                children[nutrient.parent_id].append(nutrient_id)
        
        # Populate the child_ids for each nutrient
        for nutrient_id, nutrient in nutrients.items():
            nutrient.child_ids = children.get(nutrient_id, [])
        
        return nutrients
    
    def read_ingredient_nutrient_quantities(
        self, ingredient_id: int
    ) -> dict[int, IngredientNutrientQuantity]:
        """Returns the nutrient quantities for the given ingredient.
        Args:
            ingredient_id (int): The id of the ingredient.
        Returns:
            dict[int, IngredientNutrientQuantity]: A dictionary of nutrient quantities, where the key is the
            id of each specific nutrient quantity.
        """
        # Init a dict to hold the nutrient quantities
        nutrient_quantities: dict[int, IngredientNutrientQuantity] = {}
        # Fetch the raw data from the repo
        raw_nutrient_quantities = self._repository.read_ingredient_nutrient_quantities(
            ingredient_id
        )
        # Cycle through the raw data
        for nutrient_id, nutrient_qty_data in raw_nutrient_quantities.items():
            # And add the data to the dict
            nutrient_quantities[nutrient_id] = IngredientNutrientQuantity(
                id=nutrient_qty_data["id"],
                nutrient_id=nutrient_id,
                entity_id=ingredient_id,
                ntr_mass_value=nutrient_qty_data["ntr_mass_value"],
                ntr_mass_unit_id=nutrient_qty_data["ntr_mass_unit_id"],
                ingredient_grams_qty=nutrient_qty_data["ing_grams_value"],
            )
        return nutrient_quantities
    
    def update_ingredient_nutrient_quantity(self, ing_nutr_qty: IngredientNutrientQuantity) -> None:
        """Updates the nutrient quantity in the database.
        Args:
            ing_nutr_qty (EntityNutrientQuantity): The nutrient quantity object.
        """
        # Raise an exception if the parent entity ID is not set
        if ing_nutr_qty.parent_entity_id is None:
            raise ValueError("The parent entity ID must be set.")
        # Update the nutrient quantity in the database
        self._repository.update_ingredient_nutrient_quantity(
            ingredient_id=ing_nutr_qty.parent_entity_id,
            global_nutrient_id=ing_nutr_qty.nutrient_id,
            ntr_mass_qty=ing_nutr_qty.nutrient_mass_value,
            ntr_mass_unit_id=ing_nutr_qty.nutrient_mass_unit_id,
            ing_grams_qty=ing_nutr_qty.entity_grams_value,
        )

        # Emit the signal for the ingredient nutrients change
        self.ingredientNutrientsChanged.emit()

    def _cache_global_nutrient_id_name_map(self) -> None:
        """Caches the global nutrient id-name map."""
        # If the map is None, init it
        if self._global_nutrient_id_name_map is None:
            self._global_nutrient_id_name_map = Map(one_to_one=True)

        # Fetch all the global nutrients
        nutrients = self.read_all_global_nutrients()

        # Add the nutrients to the map
        for nutrient_id, nutrient in nutrients.items():
            self._global_nutrient_id_name_map.add_mapping(key=nutrient_id, value=nutrient.nutrient_name)