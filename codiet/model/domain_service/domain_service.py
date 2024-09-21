
from typing import Tuple, Mapping, TYPE_CHECKING

from codiet.utils import IUC, SingletonMeta

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversion
    from codiet.model.flags import FlagDefinition
    from codiet.model.nutrients import Nutrient

class DomainService(metaclass=SingletonMeta):

    def __init__(
        self, 
        units: Mapping[str, 'Unit'],
        global_unit_conversions: Mapping[Tuple[str, str], 'UnitConversion'],
        flag_definitions: Mapping[str, 'FlagDefinition'], 
        nutrients: Mapping[str, 'Nutrient'],
    ) -> None:
        self._units = units
        self._global_unit_conversions = global_unit_conversions
        self._flag_definitions = flag_definitions
        self._nutrients = nutrients

        self._gram = self._units['gram']

    @property
    def units(self) -> IUC['Unit']:
        return IUC(self._units.values())

    @property
    def gram(self) -> 'Unit':
        return self._gram

    @property
    def global_unit_conversions(self) -> IUC['UnitConversion']:
        return IUC(self._global_unit_conversions.values())
    
    @property
    def flag_definitions(self) -> IUC['FlagDefinition']:
        return IUC(self._flag_definitions.values())

    @property
    def flag_names(self) -> IUC[str]:
        return IUC(self._flag_definitions.keys())

    @property
    def nutrients(self) -> IUC['Nutrient']:
        return IUC(self._nutrients.values())

    def get_unit(self, name: str) -> 'Unit':
        return self._units[name]

    def get_flag_definition(self, name: str) -> 'FlagDefinition':
        return self._flag_definitions[name]
    
    def get_nutrient(self, name: str) -> 'Nutrient':
        return self._nutrients[name]