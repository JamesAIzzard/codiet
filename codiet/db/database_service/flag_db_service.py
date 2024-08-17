from typing import Collection, TYPE_CHECKING

from PyQt6.QtCore import pyqtSignal

from codiet.db.database_service.database_service_base import DatabaseServiceBase

from codiet.utils.map import Map
from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.utils.unique_collection import MutableUniqueCollection as MUC
from codiet.models.flags.flag import Flag
from codiet.models.flags.ingredient_flag import IngredientFlag
if TYPE_CHECKING:
    from codiet.models.ingredients.ingredient import Ingredient

class FlagDBService(DatabaseServiceBase):
    """Database service module for flags."""

    ingredientFlagsChanged = pyqtSignal()
    globalFlagsChanged = pyqtSignal()

    def __init__(self, *args, **kwargs) -> None:
        """Initialise the flag database service."""
        super().__init__(*args, **kwargs)

        # Cache the global flag id-name map
        self._global_flag_id_name_map:Map[int, str]|None = None
        self._global_flags: IUC[Flag]|None = None

    @property
    def flag_id_name_map(self) -> Map[int, str]:
        """Get the global flag id-name map."""
        if self._global_flag_id_name_map is None:
            self._reset_global_flags_cache()
        return self._global_flag_id_name_map # type: ignore # checked in the property setter
    
    @property
    def global_flags(self) -> IUC[Flag]:
        """Get the global flags."""
        if self._global_flags is None:
            self._reset_global_flags_cache()
        return self._global_flags # type: ignore # checked in the property setter

    def get_flag_by_name(self, flag_name: str) -> Flag:
        """Get the flag by name."""
        for flag in self.global_flags:
            if flag.flag_name.lower().strip() == flag_name.lower().strip():
                return flag
        raise ValueError(f"Flag with name {flag_name} not found.")

    def get_flag_by_id(self, flag_id: int) -> Flag:
        """Get the flag by ID."""
        for flag in self.global_flags:
            if flag.id == flag_id:
                return flag
        raise ValueError(f"Flag with ID {flag_id} not found.")

    def create_global_flag(self, flag: Flag, _signal: bool=True) -> Flag:
        """Insert the global flags into the database."""
        # Create the flag
        flag_id = self._repository.flags.create_flag(
            flag_name=flag.flag_name
        )

        # Update the ID of the flag
        flag.id = flag_id

        if _signal:
            # Rebuild the cache and emit the signal
            self._reset_global_flags_cache()
            self.globalFlagsChanged.emit()

        return flag

    def create_global_flags(self, flags: Collection[Flag]) -> IUC[Flag]:
        """Insert the global flags into the database."""
        # Init a list to store the saved flags
        saved_flags = []

        for flag in flags:
            saved_flags.append(self.create_global_flag(flag, _signal=False))
        
        # Rebuild the cache and emit the signal
        self._reset_global_flags_cache()
        self.globalFlagsChanged.emit()

        return IUC(saved_flags)

    def create_ingredient_flag(self, ingredient_flag: IngredientFlag, _signal:bool = True) -> IngredientFlag:
        """Insert the ingredient flags into the database."""
        # Check the ingredient ID is populated
        if ingredient_flag.ingredient.id is None:
            raise ValueError("The ingredient ID must be populated to create an ingredient flag.")
        
        # Check the flag ID is populated
        if ingredient_flag.flag.id is None:
            raise ValueError("The flag ID must be populated to create an ingredient flag.")

        ingredient_flag_id = self._repository.flags.create_ingredient_flag(
            ingredient_id=ingredient_flag.ingredient.id,
            flag_id=ingredient_flag.flag.id,
            flag_value=ingredient_flag.flag_value
        )
        ingredient_flag.id = ingredient_flag_id

        if _signal:
            self.ingredientFlagsChanged.emit()

        return ingredient_flag

    def create_ingredient_flags(self, flags: Collection[IngredientFlag]) -> IUC[IngredientFlag]:
        """Insert the ingredient flags into the database."""
        # Init a list to store the saved flags
        saved_flags = []

        for flag in flags:
            saved_flags.append(self.create_ingredient_flag(flag, _signal=False))

        # Emit the signal for the ingredient flags change
        self.ingredientFlagsChanged.emit()

        return IUC(saved_flags)
    
    def read_all_global_flags(self) -> IUC[Flag]:
        """Read all global flags from the database."""
        global_flags = self._repository.flags.read_all_global_flag_names()

        flags = []

        for flag_id, flag_name in global_flags.items():
            flags.append(
                Flag(
                    id=flag_id,
                    flag_name=flag_name
                )
            )

        return IUC(flags)

    def read_ingredient_flags(self, ingredient: 'Ingredient') -> IUC[IngredientFlag]:
        """Read the flags for the given ingredient."""
        assert ingredient.id is not None
        flags_data = self._repository.flags.read_ingredient_flags(ingredient.id)

        flags = []

        for uid, fd in flags_data.items():
            # Grab the flag object
            flag = self.get_flag_by_id(fd["flag_id"])

            # Construct the ingredient flag
            ing_flag = IngredientFlag(
                id=uid,
                ingredient=ingredient,
                flag=flag,
                flag_value=fd["flag_value"]
            )

            flags.append(ing_flag)

        return IUC(flags)
    
    def update_ingredient_flag(self, ingredient_flag: IngredientFlag, _signal=True) -> None:
        """Update the flag for the given ingredient."""
        # Check the ingredient ID and flag ID are populated
        if ingredient_flag.ingredient.id is None or ingredient_flag.flag.id is None:
            raise ValueError("The ingredient ID and flag ID must be populated to update an ingredient flag.")
        
        self._repository.flags.update_ingredient_flag(
            ingredient_id=ingredient_flag.ingredient.id,
            flag_id=ingredient_flag.flag.id,
            flag_value=ingredient_flag.flag_value
        )

        # Emit the signal for the ingredient flags change
        self.ingredientFlagsChanged.emit()

    def update_ingredient_flags(self, flags: Collection[IngredientFlag]) -> None:
        """Update the flags for the given ingredient."""
        for flag in flags:
            self.update_ingredient_flag(flag, _signal=False)

    def delete_ingredient_flag(self, ingredient_flag: IngredientFlag, _signal=True) -> None:
        """Delete the flag for the given ingredient."""
        # Check the ingredient ID and flag ID are populated
        if ingredient_flag.ingredient.id is None or ingredient_flag.flag.id is None:
            raise ValueError("The ingredient ID and flag ID must be populated to delete an ingredient flag.")
        
        self._repository.flags.delete_ingredient_flag(
            ingredient_id=ingredient_flag.ingredient.id,
            flag_id=ingredient_flag.flag.id
        )

        # Emit the signal for the ingredient flags change
        self.ingredientFlagsChanged.emit()

    def delete_ingredient_flags(self, flags: Collection[IngredientFlag]) -> None:
        """Delete the flags supplied."""
        for flag in flags:
            self.delete_ingredient_flag(flag, _signal=False)

    def _reset_global_flags_cache(self) -> None:
        """Re(generates) the global flag caches."""

        # Instantiate if None
        if self._global_flags is None:
            self._global_flags = IUC[Flag]()

        if self._global_flag_id_name_map is None:
            self._global_flag_id_name_map = Map[int, str](one_to_one=True)

        # Reset the caches
        # Clear instead of replace, so existing references still work.
        self._global_flags._clear()
        self._global_flag_id_name_map.clear()

        # Read the global flags from the database
        global_flags = MUC(self.read_all_global_flags())

        # Rebuild the ID-name mape
        for flag in global_flags:
            assert flag.id is not None
            self._global_flag_id_name_map.add_mapping(key=flag.id, value=flag.flag_name)

        # Rebuild the global flags cache
        for flag in global_flags:
            self._global_flags._add(flag)
        