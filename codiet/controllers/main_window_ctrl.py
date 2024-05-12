from codiet.utils.search import filter_text
from codiet.db.database_service import DatabaseService
from codiet.views.search_views import SearchPopupView
from codiet.views.dialog_box_view import ErrorDialogBoxView
from codiet.views.main_window_view import MainWindowView
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.recipe_editor_view import RecipeEditorView
from codiet.views.recipe_types_editor_view import RecipeTypesEditorView
from codiet.views.goal_set_editor_view import GoalSetEditorView
from codiet.controllers.ingredient_editor_ctrl import IngredientEditorCtrl
from codiet.controllers.recipe_editor_ctrl import RecipeEditorCtrl


class MainWindowCtrl:
    """The main window controller for the CoDiet application."""

    def __init__(self, view: MainWindowView):
        self.view = view  # stash the main window view

        # Add the pages to the view
        self.view.add_page("ingredient-editor", IngredientEditorView())
        self.view.add_page("recipe-editor", RecipeEditorView())
        self.view.add_page("recipe-types-editor", RecipeTypesEditorView())
        self.view.add_page("goal-set-editor", GoalSetEditorView())

        # Init popup windows
        self.ingredient_search_popup = SearchPopupView(
            title="Search Ingredients"
        )
        self.recipe_search_popup = SearchPopupView(
            title="Search Recipes"
        )
        self.error_popup = ErrorDialogBoxView(parent=self.view)

        # Instantiate the controllers
        self.ingredient_editor_ctrl = IngredientEditorCtrl(self.view.pages["ingredient-editor"])
        self.recipe_editor_ctrl = RecipeEditorCtrl(self.view.pages["recipe-editor"])

        # Connect up the signals
        self._connect_menu_bar_signals()
        self._connect_ingredient_search_signals()
        self._connect_recipe_search_signals()

        # Cache names for search
        self.ingredient_names = []
        self.recipe_names = []

        # Since the ingredient editor is showing first, 
        # load an ingredient instance into the editor
        with DatabaseService() as db_service:
            self.ingredient_editor_ctrl.load_ingredient_instance(
                db_service.create_empty_ingredient()
            )

    def _on_new_ingredient_clicked(self):
        """Handle the user clicking the New Ingredient button."""
        # Put a new ingredient in the editor
        with DatabaseService() as db_service:
            self.ingredient_editor_ctrl.load_ingredient_instance(
                db_service.create_empty_ingredient()
            )
        # Show the editor
        self.view.show_page("ingredient-editor")

    def _on_edit_ingredient_clicked(self) -> None:
        """Handle the user clicking the Edit Ingredient button on the menubar."""
        # Cache the ingredient names for the search popup
        with DatabaseService() as db_service:
            self.ingredient_names = db_service.fetch_all_ingredient_names()
        # Show the search popup
        self.ingredient_search_popup.exec()

    def _on_ingredient_search_term_changed(self, search_term: str) -> None:
        """Handle the user changing the search term in the ingredient search popup."""
        # Filter the ingredient names
        matching_ingredient_names = filter_text(search_term, self.ingredient_names, 5)
        # Update the search results
        self.ingredient_search_popup.update_results_list(matching_ingredient_names)

    def _on_ingredient_search_term_cleared(self) -> None:
        """Handle the user clearing the search term in the ingredient search popup."""
        # Clear the search results
        self.ingredient_search_popup.clear_results_list()
        # Clear the search term
        self.ingredient_search_popup.clear_search_term()

    def _on_ingredient_selected_for_edit(self, ingredient_name: str) -> None:
        """Handle the user selecting an ingredient to edit in search results."""
        # Fetch the ingredient
        with DatabaseService() as db_service:
            ingredient = db_service.fetch_ingredient_by_name(ingredient_name)
        # Load it into the editor
        self.ingredient_editor_ctrl.load_ingredient_instance(ingredient)
        # Show the editor
        self.view.show_page("ingredient-editor")
        # Close the search popup
        self.ingredient_search_popup.close()

    def _on_delete_ingredient_clicked(self):
        """Handle the user clicking the Delete Ingredient button."""
        # Configure error box to say not implemented
        raise NotImplementedError("Delete Ingredient functionality not yet implemented.")

    def _on_new_recipe_clicked(self):
        """Handle the user clicking the New Recipe button."""
        # Put a new recipe in the editor
        with DatabaseService() as db_service:
            self.recipe_editor_ctrl.load_recipe_instance(
                db_service.create_empty_recipe()
            )
        # Show the editor
        self.view.show_page("recipe-editor")

    def _on_edit_recipe_clicked(self):
        """Handle the user clicking the Edit Recipe button."""
        # Cache the recipe names for the search popup
        with DatabaseService() as db_service:
            self.recipe_names = db_service.fetch_all_recipe_names()
        # Connect the handler to the search popup
        self.recipe_search_popup.resultSelected.connect(self._on_recipe_selected_for_edit)
        # Show the editor
        self.recipe_search_popup.show()

    def _on_recipe_search_term_changed(self, search_term):
        """Handle the user changing the search term in the recipe search popup."""
        # Filter the recipe names
        matching_recipe_names = filter_text(search_term, self.recipe_names, 5)
        # Update the search results
        self.recipe_search_popup.update_results_list(matching_recipe_names)

    def _on_recipe_search_term_cleared(self):
        """Handle the user clearing the search term in the recipe search popup."""
        # Clear the search results
        self.recipe_search_popup.clear_results_list()
        # Clear the search term
        self.recipe_search_popup.clear_search_term()

    def _on_recipe_selected_for_edit(self, recipe_name):
        """Handle the user selecting a recipe to edit in search results."""
        # Fetch the recipe
        with DatabaseService() as db_service:
            recipe = db_service.fetch_recipe_by_name(recipe_name)
        # Load it into the editor
        self.recipe_editor_ctrl.load_recipe_instance(recipe)
        # Show the editor
        self.view.show_page("recipe-editor")

    def _on_edit_recipe_types_clicked(self):
        """Handle the user clicking the Edit Recipe Types button."""
        # Configure error box to say not implemented
        raise NotImplementedError("Edit Recipe Types functionality not yet implemented.")

    def _on_new_goal_set_clicked(self):
        """Handle the user clicking the New Meal Goal button."""
        self.view.show_page("goal-set-editor")

    def _on_edit_goal_set_clicked(self):
        """Handle the user clicking the Edit Meal Goal button."""
        # Configure error box to say not implemented
        raise NotImplementedError("Edit goal set functionality not yet implemented.")

    def _on_delete_goal_set_clicked(self):
        """Handle the user clicking the Delete Meal Goal button."""
        # Configure error box to say not implemented
        raise NotImplementedError("Delete goal set functionality not yet implemented.")

    def _on_edit_goal_defaults_clicked(self):
        """Handle the user clicking the Meal Goal Defaults button."""
        # Configure error box to say not implemented
        raise NotImplementedError("Edit goal defaults functionality not yet implemented.")

    def _on_general_help_clicked(self):
        """Handle the user clicking the General Help button."""
        # Configure error box to say not implemented
        raise NotImplementedError("General help functionality not yet implemented.")

    def _connect_menu_bar_signals(self):
        """Connect the signals from the menu bar to the appropriate slots."""
        self.view.newIngredientClicked.connect(self._on_new_ingredient_clicked)
        self.view.editIngredientClicked.connect(self._on_edit_ingredient_clicked)
        self.view.deleteIngredientClicked.connect(self._on_delete_ingredient_clicked)
        self.view.newRecipeClicked.connect(self._on_new_recipe_clicked)
        self.view.editRecipeClicked.connect(self._on_edit_recipe_clicked)
        self.view.editRecipeTypesClicked.connect(self._on_edit_recipe_types_clicked)
        self.view.newGoalSetClicked.connect(self._on_new_goal_set_clicked)
        self.view.editGoalSetClicked.connect(self._on_edit_goal_set_clicked)
        self.view.deleteGoalSetClicked.connect(self._on_delete_goal_set_clicked)
        self.view.editGoalDefaultsClicked.connect(self._on_edit_goal_defaults_clicked)
        self.view.generalHelpClicked.connect(self._on_general_help_clicked)

    def _connect_ingredient_search_signals(self):
        """Connect the signals from the ingredient search popup to the appropriate slots."""
        self.ingredient_search_popup.searchTermChanged.connect(self._on_ingredient_search_term_changed)
        self.ingredient_search_popup.resultSelected.connect(self._on_ingredient_selected_for_edit)
        self.ingredient_search_popup.searchTermCleared.connect(self._on_ingredient_search_term_cleared)

    def _connect_recipe_search_signals(self):
        """Connect the signals from the recipe search popup to the appropriate slots."""
        self.recipe_search_popup.searchTermChanged.connect(self._on_recipe_search_term_changed)
        self.recipe_search_popup.resultSelected.connect(self._on_recipe_selected_for_edit)
        self.recipe_search_popup.searchTermCleared.connect(self._on_recipe_search_term_cleared)