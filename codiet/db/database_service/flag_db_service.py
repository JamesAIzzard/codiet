from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from . import DatabaseService
from ..repository import Repository
from codiet.utils.map import Map
from codiet.models.flags import Flag, EntityFlag

class FlagDBService(QObject):
    """Database service module for flags."""

    ingredientFlagsChanged = pyqtSignal()
    globalFlagsChanged = pyqtSignal()

    def __init__(self, repository: Repository, db_service: 'DatabaseService'):
        """Initialise the flag database service."""
        super().__init__()

        self._repository = repository
        self._db_service = db_service

        # Cache the global flag id-name map
        self._global_flag_id_name_map:Map[int, str]|None = None

    @property
    def flag_id_name_map(self) -> Map[int, str]:
        """Get the global flag id-name map."""
        if self._global_flag_id_name_map is None:
            self._cache_flag_id_name_map()
        return self._global_flag_id_name_map # type: ignore # checked in the property setter
    
    def create_global_flags(self, flags: list[Flag]) -> dict[int, Flag]:
        """Insert the global flags into the database.
        Args:
            flags (list[Flag]): The flags to be inserted.
        Returns:
            dict[int, Flag]: The flags that were inserted, where the key is the flag ID.
        """
        # Init a dict to store the saved flags
        saved_flags = {}

        for flag in flags:
            flag_id = self._repository.create_global_flag(
                flag_name=flag.flag_name
            )
            flag.id = flag_id
            saved_flags[flag_id] = flag
        
        # Emit the signal for the global flags change
        self.globalFlagsChanged.emit()

        return saved_flags


    def create_ingredient_flags(self, flags: list[EntityFlag]) -> dict[int, EntityFlag]:
        """Insert the ingredient flags into the database.
        Args:
            flags (list[EntityFlag]): The flags to be inserted.
        Returns:
            dict[int, EntityFlag]: The flags that were inserted, where the key is the flag ID.
        """
        # Init a dict to store the saved flags
        saved_flags = {}

        for flag in flags:
            # Check the ingredient ID is populated
            if flag.ref_entity_id is None:
                raise ValueError("The ingredient ID must be populated to create an ingredient flag.")
            
            # Check the flag ID is populated
            if flag.id is None:
                raise ValueError("The flag ID must be populated to create an ingredient flag.")

            id = self._repository.create_ingredient_flag(
                ingredient_id=flag.ref_entity_id, # UID of the ingredient
                flag_id=flag.id, # UID of the ingredient flag
                flag_value=flag.flag_value
            )
            flag.id = id
            saved_flags[id] = flag

        # Emit the signal for the ingredient flags change
        self.ingredientFlagsChanged.emit()

        return saved_flags
    
    def read_ingredient_flags(self, ingredient_id: int) -> dict[int, EntityFlag]:
        """Read the flags for the given ingredient.
        Args:
            ingredient_id (int): The ID of the ingredient to read the flags for.
        Returns:
            dict[int, EntityFlag]: The flags for the ingredient, where the key is the flag ID.
        """
        flag_data = self._repository.read_ingredient_flags(ingredient_id)

        flags = {}

        for uid, flag_value in flag_data.items():
            flags[uid] = EntityFlag(
                id=uid,
                ref_object_id=ingredient_id,
                value=flag_value
            )

        return flags
    
    def update_ingredient_flags(self, flags: list[EntityFlag]) -> None:
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

    def delete_ingredient_flags(self, flags: list[EntityFlag]) -> None:
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

    def _cache_flag_id_name_map(self) -> None:
        """Re(generates) the cached flag ID to name map
        Emits the signal for the flag ID to name map change.
        Returns:
            Map: A map associating flag ID's with names.
        """
        # Fetch all the flags
        flags = self._repository.read_all_global_flags()

        # Clear the map
        self.flag_id_name_map.clear()

        # Add each flag to the map
        for flag_id, flag_name in flags.items():
            self.flag_id_name_map.add_mapping(key=flag_id, value=flag_name)