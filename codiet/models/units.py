class CustomUnit():
    """A custom measurement unit."""
    def __init__(
            self, 
            unit_name: str, 
            custom_unit_qty: float|None = None,
            std_unit_qty: float|None = None,
            std_unit_name: str = 'g', 
            unit_id: int | None = None
        ):
        self.unit_name = unit_name
        self.custom_unit_qty = custom_unit_qty
        self.std_unit_qty = std_unit_qty
        self.std_unit_name = std_unit_name
        self.unit_id = unit_id