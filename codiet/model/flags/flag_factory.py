from typing import TYPE_CHECKING

from codiet.model.flags import Flag, FlagDefinition

if TYPE_CHECKING:
    from codiet.model.flags import FlagDTO, FlagDefinitionDTO

class FlagFactory:
    
    def create_flag_definition_from_dto(self, flag_definition_dto: "FlagDefinitionDTO") -> FlagDefinition:
        flag_definition = FlagDefinition(
            flag_name=flag_definition_dto["flag_name"],
            if_true_must_contain=flag_definition_dto["if_true_must_contain"],
            if_true_cannot_contain=flag_definition_dto["if_true_cannot_contain"],
            if_true_implies_true=flag_definition_dto["if_true_implies_true"],
            if_true_implies_false=flag_definition_dto["if_true_implies_false"],
            if_false_must_contain=flag_definition_dto["if_false_must_contain"],
            if_false_cannot_contain=flag_definition_dto["if_false_cannot_contain"],
            if_false_implies_true=flag_definition_dto["if_false_implies_true"],
            if_false_implies_false=flag_definition_dto["if_false_implies_false"],
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