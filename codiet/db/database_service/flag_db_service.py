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

    def create_ingredient_flag(self, flag: IngredientFlag, _signal:bool = True) -> IngredientFlag:
        """Insert the ingredient flags into the database."""
        # Check the ingredient ID is populated
        if flag.ingredient.id is None:
            raise ValueError("The ingredient ID must be populated to create an ingredient flag.")
        
        # Check the flag ID is populated
        if flag.id is None:
            raise ValueError("The flag ID must be populated to create an ingredient flag.")

        ingredient_flag_id = self._repository.flags.create_ingredient_flag(
            ingredient_id=flag.ingredient.id,
            flag_id=flag.id,
            flag_value=flag.flag_value
        )
        flag.id = ingredient_flag_id

        if _signal:
            self.ingredientFlagsChanged.emit()

        return flag

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

        flags = {}

        for uid, fd in flags_data.items():
            flags[uid] = IngredientFlag(
                ingredient=ingredient,
                flag_name=fd["flag_name"],
                flag_value=fd["flag_value"],
            )

        return flags
    
    def update_ingredient_flags(self, flags: list[IngredientFlag]) -> None:
        """Update the flags for the given ingredient.
        Args:
            flags (dict[int, EntityFlag]): The flags to be updated, where the key is the flag ID.
        Returns:
            dict[int, EntityFlag]: The updated flags, where the key is the flag ID.
        """
        for flag in flags:

            # Check the reference ID and flag ID are populated
            if flag.ref_entity_id is None or flag.id is None:
                raise ValueError("The ingredient ID and flag ID must be populated to update an ingredient flag.")
            
            self._repository.update_ingredient_flag(
                ingredient_id=flag.ref_entity_id,
                flag_id=flag.id,
                flag_value=flag.flag_value
            )

    def delete_ingredient_flags(self, flags: list[IngredientFlag]) -> None:
        """Delete the flags supplied.
        Args:
            flags (list[EntityFlag]): The flags to be deleted.
        """
        for flag in flags:

            # Check the flag ID is populated
            if flag.id is None:
                raise ValueError("The flag ID must be populated to delete an ingredient flag.")
            
            self._repository.delete_ingredient_flag(
                ingredient_flag_id=flag.id
            )

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
        