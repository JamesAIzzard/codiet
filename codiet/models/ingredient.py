from typing import Optional


class Ingredient:
    def __init__(self, name: Optional[str] = None):
        self.name = name
        self.id:int | None = None
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
        self.gi = None
        self.nutrients = {}

    @property
    def populated_nutrients(self) -> list[str]:
        """Returns a list of nutrients that have been populated."""
        return [ntr for ntr in self.nutrients if self.nutrients[ntr]]

    def nutrient_is_populated(self, nutrient_name: str) -> bool:
        """Returns True if the nutrient has been populated."""
        return nutrient_name in self.nutrients

    def add_nutrient_qty(
        self,
        nutrient_name: str,
        ntr_qty: float,
        ntr_qty_unit: str,
        ing_qty: float,
        ing_qty_unit: str,
    ) -> None:
        """Adds a nutrient to the ingredient."""
        self.nutrients[nutrient_name] = {
            "ntr_qty": ntr_qty,
            "ntr_qty_unit": ntr_qty_unit,
            "ing_qty": ing_qty,
            "ing_qty_unit": ing_qty_unit,
        }
