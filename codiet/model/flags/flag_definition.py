class FlagDefinition:
    
    def __init__(self, flag_name: str) -> None:
        self._flag_name = flag_name

    @property
    def flag_name(self) -> str:
        return self._flag_name