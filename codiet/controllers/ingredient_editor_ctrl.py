from typing import Optional

from codiet.db.database_service import DatabaseService
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.flag_editor_view import FlagEditorView
from codiet.controllers.flag_editor_ctrl import FlagEditorCtrl
from codiet.controllers.ingredient_nutrients_editor_ctrl import IngredientNutrientsEditorCtrl
from codiet.models.ingredient import Ingredient

class IngredientEditorCtrl:
    def __init__(self, view: IngredientEditorView, db_service:DatabaseService, ingredient:Optional[Ingredient]=None):
        self.view = view
        self.db_service = db_service

        # Init an ingredient if not provided
        if ingredient is None:
            self.ingredient = Ingredient()
        # Otherwise, use the one you were given
        else:
            self.ingredient = ingredient

        # Instantiate the ingredient flag editor controller
        self.ingredient_flag_editor_ctrl = FlagEditorCtrl(
            self.view.flag_editor_view, self.db_service
        )

        # Instantiate the ingredient nutrient editor controller
        self.ingredient_nutrients_editor_ctrl = IngredientNutrientsEditorCtrl(
            self.view.nutrient_editor_view, self.db_service
        )

        # Connect the view signals to the controller methods
        self.view.txt_ingredient_name.textChanged.connect(self.on_ingredient_name_changed)
        self.view.btn_save_ingredient.pressed.connect(self.on_save_ingredient_pressed)

    def on_ingredient_name_changed(self):
        """Handler for changes to the ingredient name."""
        # Update the ingredient name
        self.ingredient.name = self.view.txt_ingredient_name.text()

    def on_save_ingredient_pressed(self):
        """Handler for the save ingredient button."""
        # Save the ingredient to the database
        self.db_service.save_ingredient(self.ingredient)