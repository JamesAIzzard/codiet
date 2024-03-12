from typing import Optional

from codiet.db.database_service import DatabaseService
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.dialog_box_view import OkDialogBoxView, ErrorDialogBoxView
from codiet.controllers.flag_editor_ctrl import FlagEditorCtrl
from codiet.controllers.ingredient_nutrients_editor_ctrl import (
    IngredientNutrientsEditorCtrl,
)
from codiet.models.ingredient import Ingredient
from codiet.exceptions import ingredient_exceptions


class IngredientEditorCtrl:
    def __init__(
        self,
        view: IngredientEditorView,
        db_service: DatabaseService,
        ingredient: Optional[Ingredient] = None,
    ):
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
        self.view.txt_ingredient_name.textChanged.connect(
            self.on_ingredient_name_changed
        )
        self.view.txt_description.textChanged.connect(
            self.on_ingredient_description_changed
        )
        self.view.txt_cost.textChanged.connect(self.on_ingredient_cost_value_changed)
        self.view.txt_cost_quantity.textChanged.connect(
            self.on_ingredient_cost_quantity_changed
        )
        self.view.cmb_cost_qty_unit.currentTextChanged.connect(
            self.on_ingredient_cost_qty_unit_changed
        )
        self.view.btn_save_ingredient.pressed.connect(self.on_save_ingredient_pressed)

    def set_ingredient_instance(self, ingredient: Ingredient):
        """Set the ingredient instance to edit."""
        # Update the stored instance
        self.ingredient = ingredient

        # Update the view
        # Update ingredient name field
        self.view.txt_ingredient_name.setText(self.ingredient.name)

        # Update description field
        # TODO: Populate description field

    def set_ingredient_cost(
        self, 
        cost_value: float | None, 
        cost_qty_value: float | None, 
        cost_qty_unit: str
    ):
        """Set the ingredient cost."""
        # Set the actual cost value
        if cost_value is not None:
            self.view.txt_cost.setText(cost_value)
        else:
            self.view.txt_cost.clear()

        # Set the cost quantity value
        if cost_qty_value is not None:
            self.view.txt_cost_quantity.setText(cost_qty_value)
        else:
            self.view.txt_cost_quantity.clear()

        # Set the cost quantity unit
        self.view.cmb_cost_qty_unit.setCurrentText(cost_qty_unit)

    def on_ingredient_name_changed(self):
        """Handler for changes to the ingredient name."""
        # Update the ingredient name
        self.ingredient.name = self.view.txt_ingredient_name.text()

    def on_ingredient_description_changed(self):
        """Handler for changes to the ingredient description."""
        # Update the ingredient description
        self.ingredient.description = self.view.txt_description.toPlainText()

    def on_ingredient_cost_value_changed(self):
        """Handler for changes to the ingredient cost."""
        # Update the ingredient cost
        self.ingredient.cost_value = self.view.txt_cost.value

    def on_ingredient_cost_quantity_changed(self):
        """Handler for changes to the ingredient quantity associated with the cost data."""
        # Update the ingredient cost quantity
        self.ingredient.cost_qty_value = float(self.view.txt_cost_quantity.text())

    def on_ingredient_cost_qty_unit_changed(self):
        """Handler for changes to the ingredient cost unit."""
        # Update the ingredient cost unit
        self.ingredient.cost_qty_unit = self.view.cmb_cost_qty_unit.currentText()

    def on_save_ingredient_pressed(self):
        """Handler for the save ingredient button."""
        # If this has been pressed from the 'Create Ingredient' route,
        # then the edit mode will be False and the ingredient will be created.
        if self.edit_mode is False:
            try:
                # Save the ingredient to the database
                self.db_service.create_ingredient(self.ingredient)

                # Show confirm dialog box
                dialog = OkDialogBoxView(
                    message="Ingredient saved.",
                    title="Ingredient Saved",
                    parent=self.view,
                )
                _ = dialog.exec()

            except ingredient_exceptions.IngredientNameExistsError as e:
                # Create a generic error box
                dialog = ErrorDialogBoxView(
                    message=f"An ingredient called {e.ingredient_name} already exists.",
                    title="Duplicate Ingredient Name",
                    parent=self.view,
                )
                _ = dialog.exec()

            except Exception as e:
                # Create a generic error box
                dialog = ErrorDialogBoxView(
                    message="An error occurred while saving the ingredient.",
                    title="Error",
                    parent=self.view,
                )
                _ = dialog.exec()

        # If this has been pressed from the 'Edit Ingredient' route,
        # then the edit mode will be True and the ingredient will be updated.
        elif self.edit_mode is True:
            # Update the ingredient.
            try:
                # Update the ingredient in the database
                self.db_service.update_ingredient(self.ingredient)

                # Show confirm dialog box
                dialog = OkDialogBoxView(
                    message="Ingredient updated.",
                    title="Ingredient Updated",
                    parent=self.view,
                )
                _ = dialog.exec()

            except Exception as e:
                # Create a generic error box
                dialog = ErrorDialogBoxView(
                    message="An error occurred while updating the ingredient.",
                    title="Error",
                    parent=self.view,
                )
                _ = dialog.exec()
