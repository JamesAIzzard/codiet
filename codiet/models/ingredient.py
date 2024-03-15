from typing import List, Dict


class Ingredient:
    def __init__(self, name: str | None = None):
        self.name = name
        self.id: int | None = None
        self.description: str | None = None
        self.cost_unit: str = "GBP"
        self.cost_value: float | None = None
        self.cost_qty_unit: str = "g"
        self.cost_qty_value: float | None = None
        self.density_mass_unit: str = "g"
        self.density_mass_value: float | None = None
        self.density_vol_unit: str = "ml"
        self.density_vol_value: float | None = None
        self.pc_qty: float | None = None
        self.pc_mass_unit: str = "g"
        self.pc_mass_value: float | None = None
        self.flags: List[str] = []
        self.gi: float | None = None
        self.nutrients: dict[str, dict[str, float|str]] = {}

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
        ntr_qty_value: float,
        ntr_qty_unit: str,
        ing_qty_value: float,
        ing_qty_unit: str,
    ) -> None:
        """Adds a nutrient to the ingredient."""
        self.nutrients[nutrient_name] = {
            "ntr_qty_value": ntr_qty_value, # nutrient quantity
            "ntr_qty_unit": ntr_qty_unit,
            "ing_qty_value": ing_qty_value, # ingredient quantity
            "ing_qty_unit": ing_qty_unit,
        }
