class Quantity:

    def __init__(self,
            unit: str,
            value: float|None=None,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._unit:str
        self._value:float|None

    @property
    def unit(self) -> str:
        return self._unit
    
    @unit.setter
    def unit(self, unit:str):
        from codiet.data import DatabaseService
        if unit not in DatabaseService.get_units():
            raise ValueError(f"Unit {unit} not found in database")
        self._unit = unit

    @property
    def value(self) -> float:
        if self._value is None:
            raise TypeError("Value not set")
        return self._value

    @property
    def is_defined(self) -> bool:
        return self._value is not None
    
    def set_value(self, value: float|None) -> 'Quantity':
        self._value = value

        return self