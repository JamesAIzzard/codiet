from codiet.models.recipe import Recipe
from codiet.models.ingredient import Ingredient
from codiet.views.ingredients_editor_view import IngredientsEditorView
from codiet.controllers.ingredient_search_popup_ctrl import IngredientSearchPopupCtrl
from codiet.views.ingredient_search_popup_view import IngredientSearchPopupView

class IngredientsEditorCtrl():
    def __init__(self, view:IngredientsEditorView, recipe:Recipe) -> None:
        """Initialize the IngredientsEditorCtrl."""
        self.view = view
        self.recipe = recipe
        self._connect_signals_and_slots()

    def add_ingredient(self, ingredient:Ingredient) -> None:
        """Add an ingredient to the recipe."""
        self.recipe.add_ingredient(ingredient)
        self.view.update_ingredients(self.recipe.ingredients)

    def remove_ingredient(self, ingredient_id:int) -> None:
        """Remove an ingredient from the recipe."""
        # Grab the ID of the selected recipe
        self.recipe.remove_ingredient(ingredient_id)
        self.view.update_ingredients(self.recipe.ingredients)

    def on_add_ingredient_button_clicked(self) -> None:
        """Show the ingredient search popup."""
        # Initialise the ingredient search popup view and its controller
        search_popup_view = IngredientSearchPopupView()
        self.ingredient_search_popup_ctrl = IngredientSearchPopupCtrl(
            view=search_popup_view,
            on_result_click=self.add_ingredient
        )
        # Show the ingredient search popup
        search_popup_view.show()

    def on_remove_ingredient_button_clicked(self) -> None:
        """Remove an ingredient from the recipe."""
        # Grab the ID of the selected recipe
        ingredient_id = self.view.selected_ingredient_id
        # If a recipe is selected
        if ingredient_id is not None:
            # Remove the recipe
            self.remove_ingredient(ingredient_id)

    def _connect_signals_and_slots(self) -> None:
        """Connect the signals and slots."""
        self.view.btn_add_ingredient.clicked.connect(self.on_add_ingredient_button_clicked)
        self.view.btn_remove_ingredient.clicked.connect(self.on_remove_ingredient_button_clicked)
