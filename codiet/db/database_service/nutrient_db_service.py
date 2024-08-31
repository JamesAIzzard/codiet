from typing import Collection, TYPE_CHECKING

from PyQt6.QtCore import pyqtSignal

from codiet.db.database_service.database_service_base import DatabaseServiceBase
from codiet.utils.map import Map
from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.utils.unique_collection import MutableUniqueCollection as MUC
from codiet.models.nutrients.nutrient import Nutrient
from codiet.models.nutrients.ingredient_nutrient_quantity import IngredientNutrientQuantity
if TYPE_CHECKING:
    pass

class NutrientDBService(DatabaseServiceBase):
    """Database service module for nutrients."""

    ingredientNutrientsChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        """Initialise the nutrient database service."""
        super().__init__(*args, **kwargs)

        # Init the caches
        self._global_nutrient_id_name_map:Map[int, str]|None = None
        self._global_nutrients: IUC[Nutrient]|None = None

    @property
    def global_nutrient_id_name_map(self) -> Map[int, str]:
        """Get the global nutrient id-name map.
        Caches the map if it is not already cached. Returns from
        the cache otherwise.
        """
        if self._global_nutrient_id_name_map is None:
            self._reset_global_nutrients_cache()
        return self._global_nutrient_id_name_map # type: ignore # checked in the property setter

    @property
    def global_nutrients(self) -> IUC[Nutrient]:
        """Get the global nutrients.
        Caches the nutrients if they are not already cached. Returns from
        the cache otherwise.
        """
        if self._global_nutrients is None:
            self._reset_global_nutrients_cache()
        return self._global_nutrients # type: ignore # checked in the property setter

    def get_nutrient_by_name(self, nutrient_name: str) -> Nutrient:
        """Get the nutrient by name."""
        for nutrient in self.global_nutrients:
            if nutrient.nutrient_name.lower().strip() == nutrient_name.lower().strip():
                return nutrient
        raise ValueError(f"Nutrient with name {nutrient_name} not found.")
    
    def get_nutrient_by_id(self, nutrient_id: int) -> Nutrient:
        """Get the nutrient by ID."""
        for nutrient in self.global_nutrients:
            if nutrient.id == nutrient_id:
                return nutrient
        raise ValueError(f"Nutrient with ID {nutrient_id} not found.")

    def create_global_nutrient(self, nutrient: Nutrient, _signal: bool=True) -> Nutrient:
        """Insert the global nutrients into the database."""
        # Stash the ID of the parent nutrient if it exists
        parent_id = None
        if nutrient.is_parent:
            parent_id = nutrient.parent.id # type: ignore # not none because is_parent is true
        
        # Create the base nutrient
        nutrient_id = self._repository.nutrients.create_global_nutrient(
            nutrient_name=nutrient.nutrient_name,
            parent_id=parent_id,
        )

        # Update the ID
        nutrient.id = nutrient_id

        # Add any aliases
        for alias in nutrient.aliases:
            self._repository.nutrients.create_global_nutrient_alias(
                primary_nutrient_id=nutrient_id,
                alias=alias,
            )

        if _signal:
            # Rebuild the cache and emit the signal
            self._reset_global_nutrients_cache()
            # If we ever allow global nutrients to be updated, we need to
            # emit a signal here.

        return nutrient

    def create_global_nutrients(self, nutrients: Collection[Nutrient]) -> IUC[Nutrient]:
        """Insert the global nutrients into the database."""
        # Init a list to store the saved nutrients
        saved_nutrients = IUC()

        for nutrient in nutrients:
            saved_nutrients._add(self.create_global_nutrient(nutrient, _signal=False))
        
        # Rebuild the cache and emit the signal
        self._reset_global_nutrients_cache()
        # If we ever allow global nutrients to be updated, we need to
        # emit a signal here.

        return saved_nutrients

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
    
    def read_all_global_nutrients(self) -> IUC[Nutrient]:
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

    def _reset_global_nutrients_cache(self) -> None:
        """(Re)generates the global nutrient caches.
        Note:
            Does not destroy the existing data structures, so that anything
            that is currently referencing them will not be affected.
        """
        # Instantiate if None
        if self._global_nutrient_id_name_map is None:
            self._global_nutrient_id_name_map = Map()
        if self._global_nutrients is None:
            self._global_nutrients = IUC()

        # Reset the caches
        # Clear instead of replace, so existing references still work.
        self._global_nutrient_id_name_map.clear()
        self._global_nutrients._clear()

        # Read the global nutrients from the database
        global_nutrients = self.read_all_global_nutrients()

        # Populate the caches
        for nutrient in global_nutrients:
            assert nutrient.id is not None
            self._global_nutrient_id_name_map[nutrient.id] = nutrient.nutrient_name
            self._global_nutrients._add(nutrient)