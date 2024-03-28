from codiet.views.ingredient_nutrients_editor_view import IngredientNutrientsEditorView
from codiet.models.ingredient import Ingredient
from codiet.utils.search import filter_text
from codiet.utils.pyqt import block_signals


class IngredientNutrientsEditorCtrl:
    """Controller for the IngredientNutrientsEditorView."""

    def __init__(self, view: IngredientNutrientsEditorView):
        self.view = view

        # Init the list of all nutrient names on the model
        self.all_nutrient_names: list[str] = []

        # Connect signals
        self.view.chk_hide_completed.stateChanged.connect(
            self.on_hide_completed_changed
        )
        self.view.txt_filter.textChanged.connect(self.on_nutrient_filter_changed)
        self.view.btn_clear_filter.clicked.connect(self.on_clear_filter_clicked)

    @property
    def filtered_nutrients(self) -> list[str]:
        """Returns a list of nutrients that match the filter."""
        # Grab the filter text
        search_term = self.view.txt_filter.text().lower()
        # Strip whitespace
        search_term = search_term.strip()
        # If filter is empty, return all nutrients
        if not search_term:
            return self.all_nutrient_names
        else:
            # Filter the nutrients
            return filter_text(search_term, self.all_nutrient_names, 3)

    def set_model(self, ingredient: Ingredient) -> None:
        """Sets the ingredient model."""
        self.ingredient = ingredient
        # Load all nutrient names into the cache
        self.all_nutrient_names = list(self.ingredient.nutrients.keys())
        # Update the view with each of these nutrient names
        for nutrient in self.all_nutrient_names:
            self.view.add_nutrient(nutrient)

    def update_nutrient_visibility(self) -> None:
        """Updates the visibility of nutrients based on the filter and hide completed settings."""
        # Start by removing all nutrients
        self.view.remove_all_nutrients()
        # Grab the filtered nutrients
        filtered_nutrients = self.filtered_nutrients
        # If 'Hide Completed' is not checked, show all filtered nutrients
        if not self.view.chk_hide_completed.isChecked():
            for nutrient in filtered_nutrients:
                self.view.add_nutrient(nutrient)
        # If 'Hide Completed' is checked, only show nutrients that are not populated
        else:
            # If nutrient is populated, hide it
            for nutrient in filtered_nutrients:
                if self.ingredient.nutrient_is_populated(nutrient):
                    self.view.remove_nutrient(nutrient)

    def on_hide_completed_changed(self) -> None:
        """Filters the nutrient list based on the 'Hide Completed' checkbox."""
        self.update_nutrient_visibility()

    def on_nutrient_filter_changed(self) -> None:
        """Filters the nutrient list based on the filter text."""
        self.update_nutrient_visibility()

    def on_clear_filter_clicked(self) -> None:
        """Clears the nutrient filter."""
        self.view.txt_filter.clear()
        self.update_nutrient_visibility()
