from typing import Union, TYPE_CHECKING

from codiet.models.flags import HasSettableFlags

if TYPE_CHECKING:
    from codiet.db.database_service import DatabaseService


class Ingredient(HasSettableFlags):
    def __init__(self):
        self.name: str | None = None
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
        self._flags: dict[str, bool] = {}
        self.gi: float | None = None
        self.nutrients: dict[str, dict] = {}

    @property
    def populated_nutrients(self) -> list[str]:
        """Returns a list of nutrients that have been populated."""
        return [ntr for ntr in self.nutrients if self.nutrient_is_populated(ntr)]

    @property
    def flags(self) -> dict[str, bool]:
        """Returns the flags."""
        return self._flags

    def set_flags(self, flags: dict[str, bool]) -> None:
        """Sets the flags."""
        self._flags.update(flags)

    def nutrient_is_populated(self, nutrient_name: str) -> bool:
        """Returns True if the nutrient has been populated."""
        if self.nutrients[nutrient_name]["ntr_qty_value"] is None:
            return False
        if self.nutrients[nutrient_name]["ntr_qty_unit"] is None:
            return False
        else:
            return True

    def update_nutrient_quantity(
        self,
        nutrient_name: str,
        ntr_qty_unit: str,
        ing_qty_unit: str,
        ntr_qty_value: float | None = None,
        ing_qty_value: float | None = None,        
    ) -> None:
        """Adds a nutrient to the ingredient."""
        if ntr_qty_value is not None:
            self.nutrients[nutrient_name]["ntr_qty_value"] = ntr_qty_value
        if ntr_qty_unit is not None:
            self.nutrients[nutrient_name]["ntr_qty_unit"] = ntr_qty_unit
        if ing_qty_value is not None:
            self.nutrients[nutrient_name]["ing_qty_value"] = ing_qty_value
        if ing_qty_unit is not None:
            self.nutrients[nutrient_name]["ing_qty_unit"] = ing_qty_unit
