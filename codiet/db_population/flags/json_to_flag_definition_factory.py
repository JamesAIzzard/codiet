from codiet.db_population import JSONToObjectFactory
from codiet.model.flags import FlagDefinition

class JSONToFlagDefinitionFactory(JSONToObjectFactory[FlagDefinition]):
    
    def build(self, flag_name: str, flag_data: dict) -> FlagDefinition:
        must_contain = flag_data.get("must_contain", [])
        cannot_contain = flag_data.get("cannot_contain", [])
        implies = flag_data.get("implies", [])
        
        return FlagDefinition(
            flag_name=flag_name,
            must_contain=must_contain,
            cannot_contain=cannot_contain,
            implies=implies
        )