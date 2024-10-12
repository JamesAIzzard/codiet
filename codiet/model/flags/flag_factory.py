from typing import TYPE_CHECKING

from codiet.model.flags import Flag, FlagDefinition

if TYPE_CHECKING:
    from codiet.model.flags import FlagDTO, FlagDefinitionDTO

class FlagFactory:
    
    def create_flag_definition_from_dto(self, flag_definition_dto: "FlagDefinitionDTO") -> FlagDefinition:
        flag_definition = FlagDefinition(
            flag_name=flag_definition_dto["flag_name"],
            must_contain=flag_definition_dto["must_contain"],
            cannot_contain=flag_definition_dto["cannot_contain"],
            implies=flag_definition_dto["implies"],
        )
        return flag_definition

    def create_flag_from_dto(self, flag_dto: "FlagDTO") -> Flag:
        flag = Flag(
            name=flag_dto["name"],
            value=flag_dto["value"],
        )
        return flag
    
    def create_flag(self, name: str, value: bool|None=None) -> Flag:
        flag = Flag(
            name=name,
            value=value,
        )
        return flag