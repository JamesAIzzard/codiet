from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject

from codiet.db.repository import Repository

if TYPE_CHECKING:
    from . import DatabaseService

class DatabaseServiceBase(QObject):

    def __init__(self, repository: Repository, db_service:'DatabaseService') -> None:
        super().__init__()
        
        self._repository = repository
        self._db_service = db_service