import typing

class NutrientRatioData(typing.TypedDict):
    nutrient_mass: typing.Optional[float]
    nutrient_mass_unit: str
    ingredient_qty: typing.Optional[float]
    ingredient_qty_unit: str