from typing import Optional

from codiet.db.database_service import DatabaseService
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.dialog_box_view import OkDialogBoxView, ErrorDialogBoxView
from codiet.controllers.flag_editor_ctrl import FlagEditorCtrl
from codiet.controllers.ingredient_nutrients_editor_ctrl import (
    IngredientNutrientsEditorCtrl,
)
from codiet.models.ingredient import Ingredient, create_ingredient
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
            self.ingredient = create_ingredient(db_service)
        # Otherwise, use the one you were given
        else:
            self.ingredient = ingredient

        # Instantiate the ingredient flag editor controller
        self.ingredient_flag_editor_ctrl = FlagEditorCtrl(
            self.view.flag_editor_view, self.ingredient
        )

        # Instantiate the ingredient nutrient editor controller
        self.ingredient_nutrients_editor_ctrl = IngredientNutrientsEditorCtrl(
            self.view.nutrient_editor_view, self.db_service
        )

        # Connect the view signals to the controller methods

        # Connect the name field
        self.view.txt_ingredient_name.textChanged.connect(
            self.on_ingredient_name_changed
        )

        # Connect the description field
        self.view.txt_description.textChanged.connect(
            self.on_ingredient_description_changed
        )

        # Connect the cost fields
        self.view.txt_cost.textChanged.connect(self.on_ingredient_cost_value_changed)
        self.view.txt_cost_quantity.textChanged.connect(
            self.on_ingredient_cost_quantity_changed
        )
        self.view.cmb_cost_qty_unit.currentTextChanged.connect(
            self.on_ingredient_cost_qty_unit_changed
        )

        # Connect the density fields
        self.view.txt_dens_vol.textChanged.connect(
            self.on_ingredient_density_vol_value_changed
        )
        self.view.cmb_dens_vol_unit.currentTextChanged.connect(
            self.on_ingredient_density_vol_unit_changed
        )
        self.view.txt_dens_mass.textChanged.connect(
            self.on_ingredient_density_mass_value_changed
        )
        self.view.cmb_dens_mass_unit.currentTextChanged.connect(
            self.on_ingredient_density_mass_unit_changed
        )

        # Connect the piece mass fields
        self.view.txt_num_pieces.textChanged.connect(
            self.on_ingredient_num_pieces_changed
        )
        self.view.txt_pc_mass_value.textChanged.connect(
            self.on_ingredient_pc_mass_value_changed
        )
        self.view.cmb_pc_mass_unit.currentTextChanged.connect(
            self.on_ingredient_pc_mass_unit_changed
        )

        # Connect the GI field
        self.view.txt_gi.textChanged.connect(self.on_gi_value_changed)

        # Connect the save button
        self.view.btn_save_ingredient.pressed.connect(self.on_save_ingredient_pressed)

    def load_ingredient_instance(self, ingredient: Ingredient):
        """Set the ingredient instance to edit."""
        # Clear all fields
        self.reset_all_fields()

        # Update the stored instance
        self.ingredient = ingredient

        # Update ingredient name field
        self.view.txt_ingredient_name.setText(self.ingredient.name)

        # Update description field
        self.view.txt_description.setText(self.ingredient.description)

        # Update cost fields
        self.set_ingredient_cost(
            self.ingredient.cost_value,
            self.ingredient.cost_qty_value,
            self.ingredient.cost_qty_unit,
        )

        # Update the bulk properties fields
        self.set_density_properties(
            self.ingredient.density_vol_value,
            self.ingredient.density_vol_unit,
            self.ingredient.density_mass_value,
            self.ingredient.density_mass_unit,
        )

        # Update the piece mass fields
        self.set_piece_mass_properties(
            self.ingredient.pc_qty,
            self.ingredient.pc_mass_value,
            self.ingredient.pc_mass_unit,
        )

        # Update the instance on the flag editor
        self.ingredient_flag_editor_ctrl.set_model(self.ingredient)

        # Update the GI field
        self.set_gi_field(self.ingredient.gi)

    def set_ingredient_cost(
        self, cost_value: float | None, cost_qty_value: float | None, cost_qty_unit: str
    ):
        """Set the ingredient cost."""
        # Set the actual cost value
        if cost_value is not None:
            self.view.txt_cost.setText(cost_value, pad_decimals=2)
        else:
            self.view.txt_cost.clear()

        # Set the cost quantity value
        if cost_qty_value is not None:
            self.view.txt_cost_quantity.setText(cost_qty_value)
        else:
            self.view.txt_cost_quantity.clear()

        # Set the cost quantity unit
        self.view.cmb_cost_qty_unit.setCurrentText(cost_qty_unit)

    def set_density_properties(
        self,
        dens_vol_value: float | None,
        dens_vol_unit: str,
        dens_mass_value: float | None,
        dens_mass_unit: str,
    ):
        """Updates the UI to show the density values provided."""
        # Set the density volume value
        if dens_vol_value is not None:
            self.view.txt_dens_vol.setText(dens_vol_value)
        else:
            self.view.txt_dens_vol.clear()

        # Set the density volume unit
        self.view.cmb_dens_vol_unit.setCurrentText(dens_vol_unit)

        # Set the density mass value
        if dens_mass_value is not None:
            self.view.txt_dens_mass.setText(dens_mass_value)
        else:
            self.view.txt_dens_mass.clear()

        # Set the density mass unit
        self.view.cmb_pc_mass_unit.setCurrentText(dens_mass_unit)

    def set_piece_mass_properties(
        self, pc_quantity: float | None, pc_mass_value: float | None, pc_mass_unit: str
    ):
        """Updates the UI to show the piece mass values provided."""
        # Set the piece count value
        if pc_quantity is not None:
            self.view.txt_num_pieces.setText(pc_quantity)
        else:
            self.view.txt_num_pieces.clear()

        # Set the piece mass value
        if pc_mass_value is not None:
            self.view.txt_pc_mass_value.setText(pc_mass_value)
        else:
            self.view.txt_pc_mass_value.clear()

        # Set the piece mass unit
        self.view.cmb_pc_mass_unit.setCurrentText(pc_mass_unit)

    def set_gi_field(self, gi: float | None):
        """Updates the GI field."""
        if gi is not None:
            self.view.txt_gi.setText(gi)
        else:
            self.view.txt_gi.clear()

    def reset_all_fields(self):
        """Reset all fields in the view."""
        # Clear the ingredient name field
        self.view.txt_ingredient_name.clear()

        # Clear the description field
        self.view.txt_description.clear()

        # Clear the cost value field
        self.view.txt_cost.clear()

        # Clear the cost quantity field
        self.view.txt_cost_quantity.clear()

        # Clear the cost quantity unit field
        self.view.cmb_cost_qty_unit.setCurrentText("g")

        # Clear the density volume value field
        self.view.txt_dens_vol.clear()

        # Clear the density volume unit field
        self.view.cmb_dens_vol_unit.setCurrentText("ml")

        # Clear the density mass value field
        self.view.txt_dens_mass.clear()

        # Clear the density mass unit field
        self.view.cmb_dens_mass_unit.setCurrentText("g")

        # Clear the piece count field
        self.view.txt_num_pieces.clear()

        # Clear the piece mass value field
        self.view.txt_pc_mass_value.clear()

        # Clear the piece mass unit field
        self.view.cmb_pc_mass_unit.setCurrentText("g")

        # Clear the flags
        self.ingredient_flag_editor_ctrl.deselect_all_flags()

        # Clear the GI field
        self.view.txt_gi.clear()

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
        self.ingredient.cost_qty_value = self.view.txt_cost_quantity.value

    def on_ingredient_cost_qty_unit_changed(self):
        """Handler for changes to the ingredient cost unit."""
        # Update the ingredient cost unit
        self.ingredient.cost_qty_unit = self.view.cmb_cost_qty_unit.currentText()

    def on_ingredient_density_vol_value_changed(self):
        """Handler for changes to the ingredient density volume value."""
        # Update the ingredient density volume value
        self.ingredient.density_vol_value = self.view.txt_dens_vol.value

    def on_ingredient_density_vol_unit_changed(self):
        """Handler for changes to the ingredient density volume unit."""
        # Update the ingredient density volume unit
        self.ingredient.density_vol_unit = self.view.cmb_dens_vol_unit.currentText()

    def on_ingredient_density_mass_value_changed(self):
        """Handler for changes to the ingredient density mass value."""
        # Update the ingredient density mass value
        self.ingredient.density_mass_value = self.view.txt_dens_mass.value

    def on_ingredient_density_mass_unit_changed(self):
        """Handler for changes to the ingredient density mass unit."""
        # Update the ingredient density mass unit
        self.ingredient.density_mass_unit = self.view.cmb_dens_mass_unit.currentText()

    def on_ingredient_num_pieces_changed(self):
        """Handler for changes to the ingredient piece count."""
        # Update the ingredient piece count
        self.ingredient.pc_qty = self.view.txt_num_pieces.value

    def on_ingredient_pc_mass_value_changed(self):
        """Handler for changes to the ingredient piece mass value."""
        # Update the ingredient piece mass value
        self.ingredient.pc_mass_value = self.view.txt_pc_mass_value.value

    def on_ingredient_pc_mass_unit_changed(self):
        """Handler for changes to the ingredient piece mass unit."""
        # Update the ingredient piece mass unit
        self.ingredient.pc_mass_unit = self.view.cmb_pc_mass_unit.currentText()

    def on_gi_value_changed(self):
        """Handler for changes to the ingredient GI value."""
        # Update the ingredient GI value
        self.ingredient.gi = self.view.txt_gi.value

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
                # Create an error box for duplicate ingredient name
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
