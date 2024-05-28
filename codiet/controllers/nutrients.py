from typing import Callable

from codiet.models.nutrients import IngredientNutrientQuantity
from codiet.views.ingredient_nutrients_editor_view import IngredientNutrientsEditorView

class IngredientNutrientsEditorCtrl():
    def __init__(
            self,
            view: IngredientNutrientsEditorView,
            get_nutrient_data: Callable[[], dict[str, IngredientNutrientQuantity]],
            on_nutrient_qty_changed: Callable[[IngredientNutrientQuantity], None],
    ) -> None:
        pass