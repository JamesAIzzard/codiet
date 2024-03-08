from typing import Optional

from codiet.db.database_service import DatabaseService
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.dialog_box_view import OkDialogBoxView, ErrorDialogBoxView
from codiet.controllers.flag_editor_ctrl import FlagEditorCtrl
from codiet.controllers.ingredient_nutrients_editor_ctrl import IngredientNutrientsEditorCtrl
from codiet.models.ingredient import Ingredient
from codiet.exceptions import ingredient_exceptions

class IngredientEditorCtrl:
    def __init__(self, view: IngredientEditorView, db_service:DatabaseService, ingredient:Optional[Ingredient]=None):
        self.view = view
        self.db_service = db_service

        # Add a flag to track which mode editor is in
        self.edit_mode = False

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

    def set_ingredient_instance(self, ingredient:Ingredient):
        """Set the ingredient instance to edit."""
        # Update the stored instance
        self.ingredient = ingredient

        # Update the view
        # Update ingredient name field
        self.view.txt_ingredient_name.setText(self.ingredient.name)

        # Update description field
        # TODO: Populate description field

        # Update the cost fields
        self.view.txt_cost.setText(str(self.ingredient.cost_value))
        self.view.txt_cost_quantity.setText(str(self.ingredient.cost_qty_value))
        self.view.cmb_cost_unit.setCurrentText(self.ingredient.cost_unit)



    def on_ingredient_name_changed(self):
        """Handler for changes to the ingredient name."""
        # Update the ingredient name
        self.ingredient.name = self.view.txt_ingredient_name.text()

    def on_save_ingredient_pressed(self):
        """Handler for the save ingredient button."""
        if self.edit_mode is False:
            try:
                # Save the ingredient to the database
                self.db_service.save_ingredient(self.ingredient)

                # Show confirm dialog box
                dialog = OkDialogBoxView(message="Ingredient saved.", title="Ingredient Saved", parent=self.view)
                _ = dialog.exec()
            
            except ingredient_exceptions.IngredientNameExistsError as e:
                # Create a generic error box
                dialog = ErrorDialogBoxView(message=f'An ingredient called {e.ingredient_name} already exists.', title="Duplicate Ingredient Name", parent=self.view)
                _ = dialog.exec()

            except Exception as e:
                # Create a generic error box
                dialog = ErrorDialogBoxView(message="An error occurred while saving the ingredient.", title="Error", parent=self.view)
                _ = dialog.exec()
        elif self.edit_mode is True:
            # Update the ingredient.
            # TODO: Implement update functionality
            pass