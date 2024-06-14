class CustomUnit():
    """A custom measurement unit."""
    def __init__(
            self, 
            unit_name: str,
            unit_id: int,
            custom_unit_qty: float|None = None,
            std_unit_qty: float|None = None,
            std_unit_name: str = 'g', 
        ):
        self.unit_name = unit_name
        self.custom_unit_qty = custom_unit_qty
        self.std_unit_qty = std_unit_qty
        self.std_unit_name = std_unit_name
        self.unit_id = unit_id