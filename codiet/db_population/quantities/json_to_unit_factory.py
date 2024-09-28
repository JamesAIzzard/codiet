from typing import Any

from codiet.db_population import JSONToObjectFactory
from codiet.model.quantities import Unit

class JSONToUnitFactory(JSONToObjectFactory[Unit]):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def build(self, unit_name:str, unit_data:Any) -> Unit:
        unit = Unit(
            name=unit_name,
            type=unit_data["type"],
            singular_abbreviation=unit_data.get("single_display_name"),
            plural_abbreviation=unit_data.get("plural_display_name"),
            aliases=unit_data.get("aliases", [])
        )
        return unit
    