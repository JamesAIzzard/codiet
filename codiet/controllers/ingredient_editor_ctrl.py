from typing import Tuple

from PyQt6.QtWidgets import QListWidgetItem

from codiet.db.database_service import DatabaseService
from codiet.models.units import Unit
from codiet.models.ingredients import Ingredient
from codiet.models.nutrients import IngredientNutrientQuantity
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.dialog_box_views import (
    ErrorDialogBoxView,
    ConfirmDialogBoxView,
    EntityNameDialogView,
)
from codiet.controllers.search import SearchColumnCtrl
from codiet.controllers.entity_name_dialog_ctrl import EntityNameDialogCtrl
from codiet.controllers.units import StandardUnitEditorCtrl, UnitConversionCtrl
from codiet.controllers.flags import FlagEditorCtrl
from codiet.controllers.nutrients import NutrientQuantitiesEditorCtrl


class IngredientEditorCtrl:
    def __init__(self, view: IngredientEditorView, db_service: DatabaseService):
        """Initialize the ingredient editor controller."""
        # Store the view and database service
        self.view = view
        self.db_service = db_service
        self._ingredient: Ingredient

        # Cache some things for search and general use
        self._ingredient_name_ids = self.db_service.build_ingredient_name_id_map()
        self._global_units = self.db_service.read_all_global_units()

        # Connect the module controllers
        self.search_column_ctrl = SearchColumnCtrl(
            view=self.view.ingredient_search,
            get_searchable_strings=lambda: self._ingredient_name_ids.str_values,
            on_result_selected=self._on_ingredient_selected, # type: ignore
        )
        self.standard_unit_editor_ctrl = StandardUnitEditorCtrl(
            view=self.view.standard_unit_editor,
            unit_list=self._global_units,
            on_standard_unit_changed=lambda unit_id: setattr(
                self.ingredient, "standard_unit_id", unit_id
            ),
        )
        self.unit_conversion_ctrl = UnitConversionCtrl(
            view=self.view.unit_conversions_editor,
            on_unit_conversion_added=self._on_custom_unit_added,
            on_unit_conversion_edited=self._on_custom_unit_edited,
            on_unit_conversion_deleted=self._on_custom_unit_deleted,
        )
        self.flag_editor_ctrl = FlagEditorCtrl(
            view=self.view.flag_editor,
            get_flags=lambda: self.ingredient.flags,
            on_flag_changed=self._on_flag_changed,
        )
        self.ingredient_nutrient_editor_ctrl = NutrientQuantitiesEditorCtrl(
            view=self.view.nutrient_quantities_editor,
            get_nutrient_data=lambda: self.ingredient.nutrient_quantities,
            on_nutrient_qty_changed=self._on_nutrient_qty_changed,
        )

        # Connect the handler functions to the view signals
        self._connect_toolbar()
        self._connect_basic_info_editors()
        self.view.cost_editor.costChanged.connect(self._on_ingredient_cost_changed)
        self.view.txt_gi.textChanged.connect(self._on_gi_value_changed)

        # Load the first ingredient into the view
        self.load_ingredient_into_view(
            self.db_service.read_ingredient(
                ingredient_id=self._ingredient_name_ids.int_values[0]
            )
        )

    @property
    def ingredient(self) -> Ingredient:
        """Get the ingredient instance."""
        return self._ingredient

    def load_ingredient_into_view(self, ingredient: Ingredient) -> None:
        """Set the ingredient instance to edit.
        Stores the ingredient, and orchestrates any loading of the view,
        child controllers and their views.
        Args:
            ingredient (Ingredient): The ingredient to edit.
        Returns:
            None
        """
        # Update the stored instance
        self._ingredient = ingredient

        # Update the views
        self.view.ingredient_name = self.ingredient.name
        self.view.ingredient_description = self.ingredient.description
        # Read the default unit
        self.view.standard_unit_editor.standard_unit_id = self.ingredient.standard_unit_id
        # Update the cost fields
        self.view.cost_editor.cost_value = self.ingredient.cost_value
        self.view.cost_editor.cost_quantity_value = self.ingredient.cost_qty_value
        # If the ingredient cost unit is not None
        if self.ingredient.cost_qty_unit_id is not None:
            # Fetch the unit from the database
            cost_unit = self.db_service.read_global_unit(self.ingredient.cost_qty_unit_id)
            # Set the cost unit name
            self.view.cost_editor.cost_quantity_unit = cost_unit.plural_display_name
        # TODO: Up to here. Next up, figure out what to do with the new unit conversions here.
        # Update the measurements fields
        self.unit_conversion_ctrl.load_custom_units_into_view(ingredient.units)
        # Set the flags
        self.view.flag_editor.remove_all_flags_from_list()
        self.view.flag_editor.add_flags_to_list(list(self.ingredient.flags.keys()))
        self.view.flag_editor.update_flags(self.ingredient.flags)
        # Update the GI field
        self.view.update_gi(self.ingredient.gi)
        # Set the nutrients
        self.ingredient_nutrient_editor_ctrl.load_all_nutrient_quantities()

    def _cache_leaf_nutrient_names(self) -> None:
        """Cache the leaf nutrient names."""
        with DatabaseService() as db_service:
            self._leaf_nutrient_names = db_service.fetch_all_leaf_nutrient_names()

    def _cache_ingredient_names(self) -> None:
        """Cache the ingredient names."""
        with DatabaseService() as db_service:
            self._ingredient_name_ids = db_service.fetch_all_ingredient_names()

    def _on_ingredient_selected(self, ing_name_and_id: Tuple[str, int]) -> None:
        """Handles the user clicking on an ingredient in the search results.
        Args:
            ing_name_and_id (Tuple[str, int]): The name and ID of the selected ingredient.
        Returns:
            None
        """
        # We only need the ID to load the ingredient
        _, ingredient_id = ing_name_and_id
        # We know the id is an int, assert it
        assert isinstance(ingredient_id, int)
        # Read the ingredient from the database
        ingredient = self.db_service.read_ingredient(ingredient_id=ingredient_id)
        # Load the ingredient into the view
        self.load_ingredient_into_view(ingredient)

    def _on_add_new_ingredient_clicked(self) -> None:
        """Handler for adding a new ingredient."""
        # Open the create new ingredient dialog box
        self.ingredient_name_editor_dialog.clear()
        self.ingredient_name_editor_dialog.show()

    def _on_delete_ingredient_clicked(self) -> None:
        """Handler for deleting an ingredient."""
        # If no ingredient is selected, show the info box to tell the user
        # to select an ingredient.
        if self.view.ingredient_search.results_list.item_is_selected is False:
            # Create a dialog to tell the user they need to select an ingredient
            dialog = ErrorDialogBoxView(
                message="Please select an ingredient to delete.",
                title="No Ingredient Selected",
                parent=self.view,
            )
            dialog.okClicked.connect(lambda: dialog.hide())
            dialog.show()
        else:
            # Create the confirm dialog
            dialog = ConfirmDialogBoxView(
                message=f"Are you sure you want to delete {self.view.ingredient_search.results_list.selected_item.text()}?",  # type: ignore
                parent=self.view,
            )
            dialog.confirmClicked.connect(
                self._on_confirm_delete_ingredient_clicked.show
            )
            dialog.cancelClicked.connect(lambda: dialog.hide())

    def _on_confirm_delete_ingredient_clicked(self) -> None:
        """Handler for confirming the deletion of an ingredient."""
        # Grab the selected ingredient name from the search widget
        ingredient_name = self.view.ingredient_search.results_list.selected_item.text()  # type: ignore
        # Delete the ingredient from the database
        with DatabaseService() as db_service:
            db_service.delete_ingredient_by_name(ingredient_name)  # type: ignore
            db_service.commit()
        # Recache the ingredient names
        self._cache_ingredient_names()
        # Reset the search pane
        self.search_column_ctrl.reset_search()

    def _on_edit_ingredient_name_clicked(self) -> None:
        """Handler for editing the ingredient name."""
        # Clear the box
        self.ingredient_name_editor_dialog.clear()
        # If the ingredient has a name already, write it into the box
        if self.ingredient.name is not None:
            self.ingredient_name_editor_dialog.entity_name = self.ingredient.name
        # Show the dialog
        self.ingredient_name_editor_dialog.show()

    def _on_ingredient_name_accepted(self, name: str) -> None:
        """Handler for accepting the new ingredient name."""
        # If there is no current ingredient yet
        if self.ingredient is None:
            # Insert a new ingredient into the database
            with DatabaseService() as db_service:
                self.ingredient = db_service.insert_new_ingredient(name)
                db_service.commit()
        # Update the name on the view
        self.view.update_name(self.ingredient.name)
        # Recache the ingredient names
        self._cache_ingredient_names()
        # Reset the search pane
        self.search_column_ctrl.reset_search()
        # Clear the new ingredient dialog
        self.ingredient_name_editor_dialog.clear()
        # Hide the new ingredient dialog
        self.ingredient_name_editor_dialog.hide()

    def _on_autopopulate_ingredient_clicked(self) -> None:
        """Handler for autopopulating the ingredient."""
        raise NotImplementedError("Autopopulate ingredient not yet implemented.")

    def _on_ingredient_description_changed(self, description: str):
        """Handler for changes to the ingredient description."""
        # Update the ingredient description
        self.ingredient.description = description
        # Update the description in the database
        with DatabaseService() as db_service:
            db_service.update_ingredient_description(
                ingredient_id=self.ingredient.id,
                description=description,
            )
            db_service.commit()

    def _on_ingredient_cost_changed(
        self,
        cost_value: float | None,
        cost_qty_value: float | None,
        cost_qty_unit: str,
    ) -> None:
        """Handler for changes to the ingredient cost."""
        # Update the ingredient cost on the model
        self.ingredient.cost_value = cost_value
        self.ingredient.cost_qty_value = cost_qty_value
        self.ingredient.cost_qty_unit = cost_qty_unit
        # Update the ingredient cost in the database
        with DatabaseService() as db_service:
            db_service.update_ingredient_cost(
                ingredient_id=self.ingredient.id,
                cost_value=cost_value,
                cost_qty_value=cost_qty_value,
                cost_qty_unit=cost_qty_unit,
            )
            db_service.commit()

    def _on_flag_changed(self, flag_name: str, flag_value: bool):
        """Handler for changes to the ingredient flags."""
        # Update flag on the model
        self.ingredient.set_flag(flag_name, flag_value)
        # Update the flag in the database
        with DatabaseService() as db_service:
            db_service.update_ingredient_flag(
                ingredient_id=self.ingredient.id,
                flag_name=flag_name,
                flag_value=flag_value,
            )
            db_service.commit()

    def _on_custom_unit_added(self, unit_name: str) -> Unit:
        """Handler for adding a custom unit."""
        # Insert the custom unit into the database
        with DatabaseService() as db_service:
            custom_unit = db_service.insert_ingredient_custom_unit(
                ingredient_id=self.ingredient.id,
                unit_name=unit_name,
            )
            db_service.commit()
        # Add the custom unit to the ingredient model
        self.ingredient.add_unit(custom_unit)
        # Return the custom unit instance
        return custom_unit

    def _on_custom_unit_edited(self, custom_unit: Unit):
        """Handler for editing a custom unit."""
        # Update the custom unit on the ingredient
        self.ingredient.update_unit(custom_unit)
        # Update the custom unit in the database
        with DatabaseService() as db_service:
            db_service.update_custom_unit(custom_unit)
            db_service.commit()

    def _on_custom_unit_deleted(self, unit_id: int):
        """Handler for deleting a custom unit."""
        # Remove the custom unit from the ingredient
        self.ingredient.unit(unit_id)
        # Remove the custom unit from the database
        with DatabaseService() as db_service:
            db_service.delete_custom_unit(unit_id)
            db_service.commit()

    def _on_gi_value_changed(self, value: float | None):
        """Handler for changes to the ingredient GI value."""
        # Update the GI value on the model
        self.ingredient.gi = value
        # Update the GI value on the database
        with DatabaseService() as db_service:
            db_service.update_ingredient_gi(
                ingredient_id=self.ingredient.id,
                gi_value=value,
            )
            db_service.commit()

    def _on_nutrient_qty_changed(self, nutrient_quantity: IngredientNutrientQuantity):
        """Handler for changes to the ingredient nutrient quantities."""
        # Update the nutrient quantity on the model
        self.ingredient.upsert_nutrient_quantity(nutrient_quantity)
        # Update the nutrient quantity in the database
        with DatabaseService() as db_service:
            db_service.update_ingredient_nutrient_quantity(
                nutrient_quantity=nutrient_quantity,
            )
            db_service.commit()

    def _connect_toolbar(self) -> None:
        """Connect the toolbar button signals."""
        self.view.addIngredientClicked.connect(self._on_add_new_ingredient_clicked)
        self.view.deleteIngredientClicked.connect(self._on_delete_ingredient_clicked)
        self.view.autopopulateClicked.connect(self._on_autopopulate_ingredient_clicked)

    def _connect_basic_info_editors(self) -> None:
        """Connect the signals for the basic info editors."""
        # Connect the edit name button
        self.view.editIngredientNameClicked.connect(
            self._on_edit_ingredient_name_clicked
        )
        # Connect the description field
        self.view.ingredientDescriptionChanged.connect(
            self._on_ingredient_description_changed
        )
