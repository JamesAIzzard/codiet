from typing import TYPE_CHECKING

from codiet.model.flags import Flag

if TYPE_CHECKING:
    from codiet.model.flags import FlagDTO

class FlagFactory:
    
    def create_flag_from_dto(self, flag_dto: "FlagDTO") -> Flag:
        flag = Flag(
            name=flag_dto["name"],
            value=flag_dto["value"],
        )
        return flag