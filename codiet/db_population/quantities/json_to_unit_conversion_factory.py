from typing import TYPE_CHECKING, Callable, Any

from codiet.db_population import JSONToObjectFactory
from codiet.model.quantities import Unit, Quantity, UnitConversion

if TYPE_CHECKING:
    from codiet.model.quantities import Unit

class JSONToUnitConversionFactory(JSONToObjectFactory[UnitConversion]):
    
    def __init__(self,
        get_unit: Callable[[str], 'Unit'],
        *args, **kwargs             
    ) -> None:
        super().__init__(*args, **kwargs)

        self._get_unit = get_unit

    def build(self, unit_names:frozenset[str], conversion_data:Any) -> UnitConversion:
        indexable_names = list(unit_names)
        from_unit = self._get_unit(indexable_names[0])
        to_unit = self._get_unit(indexable_names[1])

        from_quantity = Quantity(value=conversion_data["from_quantity"], unit=from_unit)
        to_quantity = Quantity(value=conversion_data["to_quantity"], unit=to_unit)

        return UnitConversion(quantities=(from_quantity, to_quantity))