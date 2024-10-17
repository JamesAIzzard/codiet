class UnitNotFoundError(ValueError):
    def __init__(self, unit_name: str):
        self.unit_name = unit_name
        super().__init__(f"Unit not found: {unit_name}")

class UnitConversionNotFoundError(ValueError):
    def __init__(self, unit_names: frozenset[str]):
        self.unit_names = unit_names
        super().__init__(f"Unit conversion not found: {unit_names}")

class ConversionUnavailableError(ValueError):
    def __init__(self, from_unit_name: str, to_unit_name: str):
        super().__init__(
            f"No conversion available from {from_unit_name} to {to_unit_name}"
        )        