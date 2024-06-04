from codiet.models.nutrients import IngredientNutrientQuantity
from codiet.models.units import CustomUnit


class Ingredient:
    """Ingredient model."""

    def __init__(self):
        self.name: str | None = None
        self.id: int | None = None
        self.description: str | None = None
        self.cost_unit: str = "GBP"
        self.cost_value: float | None = None
        self.cost_qty_unit: str = "g"
        self.cost_qty_value: float | None = None
        self._custom_units: dict[str, CustomUnit] = {}
        self._flags: dict[str, bool] = {}
        self.gi: float | None = None
        self._nutrients: dict[str, IngredientNutrientQuantity] = {}

    @property
    def flags(self) -> dict[str, bool]:
        """Returns the flags."""
        return self._flags

    @property
    def custom_units(self) -> dict[str, CustomUnit]:
        """Returns the custom units."""
        return self._custom_units

    @property
    def nutrient_quantities(self) -> dict[str, IngredientNutrientQuantity]:
        """Returns the nutrient quantities."""
        return self._nutrients

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

    def add_custom_unit(self, custom_unit: CustomUnit) -> None:
        """Adds a custom unit."""
        self._custom_units[custom_unit.unit_name] = custom_unit

    def remove_custom_unit(self, custom_unit_name: str) -> None:
        """Removes a custom unit."""
        del self._custom_units[custom_unit_name]

    def update_custom_unit(
        self, existing_unit_name: str, custom_unit: CustomUnit
    ) -> None:
        """Updates a custom unit."""
        # Rename the custom unit if the name has changed
        if existing_unit_name != custom_unit.unit_name:
            self._custom_units[custom_unit.unit_name] = self._custom_units.pop(
                existing_unit_name
            )
        # Update the custom unit
        self._custom_units[custom_unit.unit_name] = custom_unit

    def update_nutrient_quantity(
        self, ingredient_nutrient: IngredientNutrientQuantity
    ) -> None:
        """Updates a nutrient quantity on the ingredient."""
        self._nutrients[ingredient_nutrient.nutrient_name] = ingredient_nutrient


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
