from typing import TYPE_CHECKING

from codiet.utils import SingletonMeta
from codiet.utils.unique_dict import FrozenUniqueDict
from codiet.model.nutrients import Nutrient
from .singleton_registry import SingletonRegistry

if TYPE_CHECKING:
    from .repository import Repository
    from codiet.model.quantities import Unit, UnitConversion

class DatabaseService(metaclass=SingletonMeta):

    def __init__(self, repository: 'Repository|None'=None) -> None:

        self._repository = repository

    @property
    def repository(self) -> 'Repository':
        if self._repository is None:
            raise RuntimeError("Repository not set.")
        return self._repository

    def set_repository(self, repository: 'Repository') -> None:
        self._repository = repository

    def read_unit(self, name:str) -> 'Unit':
        return self._singleton_registry.get_unit(name)
    
    def _build_unit(self, name:str) -> 'Unit':
        from codiet.model.quantities import Unit
        unit_dto = self.repository.read_unit_data(name)
        return Unit.from_dto(unit_dto)

    def read_all_global_unit_conversion_names(self) -> list[set[str]]:
        return self.repository.read_all_global_unit_conversion_names()

    def read_global_unit_conversion(self) -> 'UnitConversion':
        global_unit_conversion_names = self.repository.read_all_global_unit_conversion_names()
        global_unit_conversions = {}
        for unit_conversion_name in global_unit_conversion_names:
            unit_conversion = self.read_global_unit_conversion(unit_conversion_name)
            global_unit_conversions[unit_conversion_name] = unit_conversion
        return FrozenUniqueDict(global_unit_conversions)
    
    def read_nutrient(self, name:str) -> 'Nutrient':
        return self._singleton_registry.get_nutrient(name)
    
    def _build_nutrient(self, name:str) -> 'Nutrient':
        nutrient_dto = self.repository.read_nutrient_data(name)
        return Nutrient.from_dto(nutrient_dto)

    

