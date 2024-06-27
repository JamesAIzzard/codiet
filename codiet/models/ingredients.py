from codiet.models.nutrients import IngredientNutrientQuantity
from codiet.models.units import IngredientUnitConversion


class Ingredient:
    """Ingredient model."""

    def __init__(self, name:str, id:int):
        self.name: str = name
        self.id: int = id
        self.description: str | None = None
        self.standard_unit_id: int | None = None        
        self.cost_unit_id: int | None = None
        self.cost_value: float | None = None
        self.cost_qty_unit_id: int | None = None
        self.cost_qty_value: float | None = None
        self._unit_conversions: dict[int, IngredientUnitConversion] = {}
        self._flags: dict[int, bool|None] = {}
        self.gi: float | None = None
        self._nutrient_quantities: dict[int, IngredientNutrientQuantity] = {}

    @property
    def flags(self) -> dict[int, bool|None]:
        """Returns the flags.
        Returns:
            dict[int, bool|None]: The flags.
                Where the key is the global flag ID and the value is the flag value.
        """
        return self._flags

    @property
    def unit_conversions(self) -> dict[int, IngredientUnitConversion]:
        """Returns the unit conversions associated with this ingredient.
        Returns:
            dict[int, IngredientUnitConversion]: The unit conversions.
                Where the key is the UID for the unit conversion on
                the ingredient.
        """
        return self._unit_conversions

    @property
    def nutrient_quantities(self) -> dict[int, IngredientNutrientQuantity]:
        """Returns the nutrient quantities.
        Returns:
            dict[int, IngredientNutrientQuantity]: The nutrient quantities.
                Where the key is the gloabl nutrient ID."""
        return self._nutrient_quantities

    def add_unit_conversion(self, unit_conversion: IngredientUnitConversion) -> None:
        """Upserts a unit conversion."""
        # Raise an exception if the unit conversion is already in the list
        for uc in self._unit_conversions.values():
            if uc == unit_conversion:
                raise KeyError(f"Unit conversion '{unit_conversion.id}' already in list.")
        # If not found, add the unit conversion
        self._unit_conversions[unit_conversion.id] = unit_conversion

    def remove_unit_conversion(self, unit_id: int) -> None:
        """Delete a unit."""
        self._unit_conversions.pop(unit_id)

    def set_flag(self, flag_id: int, value: bool|None) -> None:
        """Sets a flag."""
        # Raise an  exception if the flag isn't in the flags list
        if flag_id not in self._flags:
            raise KeyError(f"Flag '{flag_id}' not in flags list.")
        # All OK, so set the flag
        self._flags[flag_id] = value

    def set_flags(self, flags: dict[int, bool|None]) -> None:
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

    def add_nutrient_quantity(
        self, ingredient_nutrient_quantity: IngredientNutrientQuantity
    ) -> None:
        """Updates a nutrient quantity on the ingredient."""
        self._nutrient_quantities[ingredient_nutrient_quantity.nutrient_id] = ingredient_nutrient_quantity


class IngredientQuantity:
    """Class to represent an ingredient quantity."""

    def __init__(
        self,
        id: int,
        ingredient_id: int,
        recipe_id: int,
        qty_value: float | None = 0.0,
        qty_unit_id: int|None = None,
        qty_utol: float | None = 0.0,
        qty_ltol: float | None = 0.0,
    ):
        """Initializes the class.
        Args:
            id (int): The ID of the ingredient quantity.
            ingredient_id (int): The ID of the ingredient.
            qty_value (float, optional): The quantity value. Defaults to 0.0.
            qty_unit_id (int, optional): The quantity unit ID. Defaults to None.
            qty_utol (float, optional): The upper tolerance. Defaults to 0.0.
            qty_ltol (float, optional): The lower tolerance. Defaults to 0.0.
        """
        self.id = id
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.qty_value = qty_value
        self.qty_unit_id = qty_unit_id
        self.upper_tol = qty_utol
        self.lower_tol = qty_ltol
