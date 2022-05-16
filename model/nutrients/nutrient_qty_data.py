import typing

class NutrientQuantityData(typing.TypedDict):
    nutrient_mass: float
    nutrient_mass_unit: str
    ingredient_qty: float
    ingredient_qty_unit: str