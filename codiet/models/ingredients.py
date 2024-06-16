from codiet.models.nutrients import IngredientNutrientQuantity
from codiet.models.units import GlobalUnit


class Ingredient:
    """Ingredient model."""

    def __init__(self, name:str, id:int):
        self.name: str = name
        self.id: int = id
        self.description: str | None = None
        self.cost_unit: str = "GBP"
        self.cost_value: float | None = None
        self.cost_qty_unit: str = "g"
        self.cost_qty_value: float | None = None
        self._custom_units: dict[int, GlobalUnit] = {}
        self._flags: dict[str, bool] = {}
        self.gi: float | None = None
        self._nutrient_quantities: dict[int, IngredientNutrientQuantity] = {}

    @property
    def flags(self) -> dict[str, bool]:
        """Returns the flags."""
        return self._flags

    @property
    def custom_units(self) -> dict[int, GlobalUnit]:
        """Returns the custom units."""
        return self._custom_units

    @property
    def nutrient_quantities(self) -> dict[int, IngredientNutrientQuantity]:
        """Returns the nutrient quantities."""
        return self._nutrient_quantities

    def add_custom_unit(self, custom_unit: GlobalUnit) -> None:
        """Adds a custom unit."""
        # Raise an exception if the custom unit is already in the custom units list
        if custom_unit.unit_id in self._custom_units:
            raise ValueError(f"Custom unit '{custom_unit.unit_id}' already in custom units list.")
        # All OK, so add the custom unit
        self._custom_units[custom_unit.unit_id] = custom_unit

    def update_custom_unit(self, custom_unit: GlobalUnit) -> None:
        """Updates a custom unit."""
        # Raise an exception if the custom unit isn't in the custom units list
        if custom_unit.unit_id not in self._custom_units:
            raise ValueError(f"Custom unit '{custom_unit.unit_id}' not in custom units list.")
        # All OK, so update the custom unit
        self._custom_units[custom_unit.unit_id] = custom_unit

    def delete_custom_unit(self, unit_id: int) -> None:
        """Delete a custom unit."""
        self._custom_units.pop(unit_id)

    def set_flag(self, flag: str, value: bool) -> None:
        """Sets a flag."""
        # Raise an  exception if the flag isn't in the flags list
        if flag not in self._flags:
            raise ValueError(f"Flag '{flag}' not in flags list.")
        # All OK, so set the flag
        self._flags[flag] = value

    def set_flags(self, flags: dict[str, bool]) -> None:
        """Sets the flags."""
        for flag, value in flags.items():
            self.set_flag(flag, value)

    def set_all_flags_true(self) -> None:
        """Sets all flags to True."""
        for flag in self._flags:
            self.set_flag(flag, True)

    def set_all_flags_false(self) -> None:
        """Sets all flags to False."""
        for flag in self._flags:
            self.set_flag(flag, False)

    def update_nutrient_quantity(
        self, ingredient_nutrient: IngredientNutrientQuantity
    ) -> None:
        """Updates a nutrient quantity on the ingredient."""
        self._nutrient_quantities[ingredient_nutrient.global_nutrient_id] = ingredient_nutrient


class IngredientQuantity:
    """Class to represent an ingredient quantity."""

    def __init__(
        self,
        ingredient: Ingredient,
        qty_value: float | None = 0.0,
        qty_unit: str = "g",
        qty_utol: float | None = 0.0,
        qty_ltol: float | None = 0.0,
    ):
        self.ingredient = ingredient
        self.qty_value = qty_value
        self.qty_unit = qty_unit
        self.upper_tol = qty_utol
        self.lower_tol = qty_ltol
