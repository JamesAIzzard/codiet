from codiet.models.recipe import Recipe
from codiet.models.ingredient import Ingredient
from codiet.views.ingredients_editor_view import IngredientsEditorView
from codiet.controllers.ingredient_search_popup_ctrl import IngredientSearchPopupCtrl

class IngredientsEditorCtrl():
    def __init__(self, view:IngredientsEditorView, recipe:Recipe) -> None:
        """Initialize the IngredientsEditorCtrl."""
        self.view = view
        self.recipe = recipe
        self._connect_signals_and_slots()

        # Instantiate the ingredient search controller
        self.ingredient_search_popup_ctrl = IngredientSearchPopupCtrl(
            view=self.view.ingredient_search_popup,
            on_result_click=self.add_ingredient
        )

    def add_ingredient(self, ingredient:Ingredient) -> None:
        """Add an ingredient to the recipe."""
        self.recipe.add_ingredient(ingredient)
        self.view.update_ingredients(self.recipe.ingredients)

    def _connect_signals_and_slots(self) -> None:
        """Connect the signals and slots."""
        self.view.btn_add_ingredient.clicked.connect(self.view.show_ingredient_search_popup)