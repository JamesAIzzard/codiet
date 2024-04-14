from codiet.db.database_service import DatabaseService
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.dialog_box_view import OkDialogBoxView, ErrorDialogBoxView
from codiet.controllers.flag_editor_ctrl import FlagEditorCtrl
from codiet.controllers.ingredient_nutrients_editor_ctrl import (
    IngredientNutrientsEditorCtrl,
)
from codiet.models.ingredient import Ingredient


class IngredientEditorCtrl:
    def __init__(
        self,
        view: IngredientEditorView,
        ingredient: Ingredient | None = None,
    ):
        self.view = view # reference to the view

        # Init an ingredient if not provided
        if ingredient is None:
            with DatabaseService() as db_service:
                self.ingredient = db_service.create_empty_ingredient()
        # Otherwise, use the one you were given
        else:
            self.ingredient = ingredient

        # Instantiate the ingredient flag editor controller
        self.ingredient_flag_editor_ctrl = FlagEditorCtrl(
            self.view.flag_editor_view, self.ingredient
        )

        # Instantiate the ingredient nutrient editor controller
        self.ingredient_nutrients_editor_ctrl = IngredientNutrientsEditorCtrl(
            self.view.nutrient_editor_view
        )

        # Load the ingredient instance
        self.load_ingredient_instance(self.ingredient)

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

        # Update the stored instance
        self.ingredient = ingredient

        # Update ingredient name field
        self.view.set_name(self.ingredient.name)

        # Update description field
        self.view.set_description(self.ingredient.description)

        # Update cost fields
        self.view.set_cost_value(self.ingredient.cost_value)
        self.view.set_cost_qty_value(self.ingredient.cost_qty_value)
        self.view.set_cost_qty_unit(self.ingredient.cost_qty_unit)

        # Update the bulk properties fields
        self.view.set_density_vol_value(self.ingredient.density_vol_value)
        self.view.set_density_vol_unit(self.ingredient.density_vol_unit)
        self.view.set_density_mass_value(self.ingredient.density_mass_value)
        self.view.set_density_mass_unit(self.ingredient.density_mass_unit)

        # Update the piece mass fields
        self.view.set_pc_qty_value(self.ingredient.pc_qty)
        self.view.set_pc_mass_value(self.ingredient.pc_mass_value)
        self.view.set_pc_mass_unit(self.ingredient.pc_mass_unit)

        # Update the instance on the flag editor
        self.ingredient_flag_editor_ctrl.set_model(self.ingredient)

        # Update the instance on the nutrient editor
        self.ingredient_nutrients_editor_ctrl.set_model(self.ingredient)

        # Update the GI field
        self.view.set_gi(self.ingredient.gi)

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
        self.ingredient.cost_value = self.view.txt_cost.text()

    def on_ingredient_cost_quantity_changed(self):
        """Handler for changes to the ingredient quantity associated with the cost data."""
        # Update the ingredient cost quantity
        self.ingredient.cost_qty_value = self.view.txt_cost_quantity.text()

    def on_ingredient_cost_qty_unit_changed(self):
        """Handler for changes to the ingredient cost unit."""
        # Update the ingredient cost unit
        self.ingredient.cost_qty_unit = self.view.cmb_cost_qty_unit.currentText()

    def on_ingredient_density_vol_value_changed(self):
        """Handler for changes to the ingredient density volume value."""
        # Update the ingredient density volume value
        self.ingredient.density_vol_value = self.view.txt_dens_vol.text()

    def on_ingredient_density_vol_unit_changed(self):
        """Handler for changes to the ingredient density volume unit."""
        # Update the ingredient density volume unit
        self.ingredient.density_vol_unit = self.view.cmb_dens_vol_unit.currentText()

    def on_ingredient_density_mass_value_changed(self):
        """Handler for changes to the ingredient density mass value."""
        # Update the ingredient density mass value
        self.ingredient.density_mass_value = self.view.txt_dens_mass.text()

    def on_ingredient_density_mass_unit_changed(self):
        """Handler for changes to the ingredient density mass unit."""
        # Update the ingredient density mass unit
        self.ingredient.density_mass_unit = self.view.cmb_dens_mass_unit.currentText()

    def on_ingredient_num_pieces_changed(self):
        """Handler for changes to the ingredient piece count."""
        # Update the ingredient piece count
        self.ingredient.pc_qty = self.view.txt_num_pieces.text()

    def on_ingredient_pc_mass_value_changed(self):
        """Handler for changes to the ingredient piece mass value."""
        # Update the ingredient piece mass value
        self.ingredient.pc_mass_value = self.view.txt_pc_mass_value.text()

    def on_ingredient_pc_mass_unit_changed(self):
        """Handler for changes to the ingredient piece mass unit."""
        # Update the ingredient piece mass unit
        self.ingredient.pc_mass_unit = self.view.cmb_pc_mass_unit.currentText()

    def on_gi_value_changed(self):
        """Handler for changes to the ingredient GI value."""
        # Update the ingredient GI value
        self.ingredient.gi = self.view.txt_gi.text()

    def on_save_ingredient_pressed(self):
        """Handler for the save ingredient button."""
        # Open the 'name required' popup if the name is empty
        if self.ingredient.name is None or self.ingredient.name.strip() == "":
            self.view.show_name_required_popup()
            return None
        # If we are saving a new ingredient (there is no ID yet)
        if self.ingredient.id is None:
            # Save it
            with DatabaseService() as db_service:
                self.ingredient.id = self.ingredient.id = db_service.insert_new_ingredient(self.ingredient)
            # Open a popup to confirm the save
            self.view.show_save_confirmation_popup()
            return None
        # So the id is populated, this must be an update.
        # First fetch the name from the database which corresponds to this id.
        with DatabaseService() as db_service:
            existing_name = db_service.fetch_ingredient_name(self.ingredient.id)
        # If the name has changed
        if existing_name != self.ingredient.name:
            # Open a yes/no popup to confirm the update
            response = self.view.show_name_change_confirmation_popup()
            # If the user clicked no, return
            if response == False:
                return None
        # If the name has not changed, go ahead and update
        with DatabaseService() as db_service:
            db_service.update_ingredient(self.ingredient)
        # Open a popup to confirm the update
        self.view.show_update_confirmation_popup()
