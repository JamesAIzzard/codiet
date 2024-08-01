from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from .database_service import DatabaseService
from .repository import Repository
from codiet.utils.map import Map

class FlagDBService(QObject):
    """Database service module for flags."""

    def __init__(self, repository: Repository, db_service: 'DatabaseService'):
        """Initialise the flag database service."""
        super().__init__()

        self.repository = repository
        self.db_service = db_service

        # Cache the global flag id-name map
        self._flag_id_name_map:Map[int, str]|None = None

    @property
    def flag_id_name_map(self) -> Map[int, str]:
        """Get the global flag id-name map."""
        if self._flag_id_name_map is None:
            self._cache_flag_id_name_map()
        return self._flag_id_name_map # type: ignore # checked in the property setter
    
    def _cache_flag_id_name_map(self) -> None:
        """Re(generates) the cached flag ID to name map
        Emits the signal for the flag ID to name map change.

        Returns:
            Map: A map associating flag ID's with names.
        """
        # Fetch all the flags
        flags = self.repository.read_all_global_flags()

        # Clear the map
        self.flag_id_name_map.clear()

        # Add each flag to the map
        for flag_id, flag_name in flags.items():
            self.flag_id_name_map.add_mapping(key=flag_id, value=flag_name)