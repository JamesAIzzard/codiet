from typing import Protocol, TYPE_CHECKING

from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC

if TYPE_CHECKING:
    from codiet.model.quantities import UnitDTO
    from codiet.model.nutrients import NutrientDTO

class Repository(Protocol):
    def read_unit_data(self, name:str) -> 'UnitDTO':...
    def read_all_global_unit_conversion_names(self) -> IUC[str]:...
    def read_nutrient_data(self, name:str) -> 'NutrientDTO':...