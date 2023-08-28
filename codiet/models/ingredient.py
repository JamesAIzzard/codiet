class Ingredient:
    def __init__(self, name: str):
        self.name = name
        self.cost_unit = None
        self.cost_value = None
        self.cost_qty_unit = None
        self.cost_qty_value = None
        self.density_mass_unit = None
        self.density_mass_value = None
        self.density_vol_unit = None
        self.density_vol_value = None
        self.pc_qty = None
        self.pc_mass_unit = None
        self.pc_mass_value = None
        self.flags = []
        self.GI = None
        self.nutrients = {}