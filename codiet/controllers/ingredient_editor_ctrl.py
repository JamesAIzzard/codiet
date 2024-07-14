from typing import Tuple

from PyQt6.QtWidgets import QWidget

from codiet.db.database_service import DatabaseService

from codiet.models.ingredients import Ingredient
from codiet.models.nutrients import filter_leaf_nutrients, IngredientNutrientQuantity
from codiet.models.units.entity_units_system import EntityUnitsSystem
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.controllers.search.search_column import SearchColumn
from codiet.controllers.dialogs.entity_name_editor_dialog import EntityNameEditorDialog
from codiet.controllers.units.standard_unit_editor import StandardUnitEditor
from codiet.controllers.units.unit_conversions_editor import UnitConversionsEditor
from codiet.controllers.cost_editor import CostEditor
from codiet.controllers.flags.flag_editor import FlagEditor
from codiet.controllers.nutrients import NutrientQuantitiesEditor


class IngredientEditor:
    def __init__(
            self,
            db_service: DatabaseService,
            view: IngredientEditorView|None = None,
            parent: QWidget|None = None
        ):
        """Initialize the ingredient editor controller."""
        # Instantiate the view if not submitted
        if view is None:
            self.view = IngredientEditorView(
                parent=parent or None
            )
        else:
            self.view = view

        # Stash constructor arguments
        self.db_service = db_service

        # Init the ingredient instance
        self._ingredient: Ingredient

        # Cache some things for search and general use
        self._ingredient_name_ids = self.db_service.build_ingredient_name_id_map()
        self._global_unit_name_ids = self.db_service.build_unit_name_id_map()
        self._global_units = self.db_service.read_all_global_units()
        self._gram_id = next(
            unit_id for unit_id, unit in self._global_units.items() if unit.unit_name == "gram"
        )
        self._global_mass_units = self.db_service.read_all_global_mass_units()
        self._global_unit_conversions = self.db_service.read_all_global_unit_conversions()
        self._flag_name_ids = self.db_service.build_flag_name_id_map()
        self._global_leaf_nutrients = filter_leaf_nutrients(
            self.db_service.read_all_global_nutrients()
        )
        self._ingredient_unit_system = EntityUnitsSystem(
            global_units=self._global_units,
            global_unit_conversions=self._global_unit_conversions,
            entity_unit_conversions={}, # Update when ingredient is loaded
        )

        # Instantiate child modules and connect signals
        # Main page components first
        # Toolbar
        self._connect_toolbar()
        # Ingredient search column
        self.ingredient_search_column = SearchColumn(
            view=self.view.ingredient_search,
            get_searchable_strings=lambda: self._ingredient_name_ids.str_values,
        )
        self.ingredient_search_column.onResultSelected.connect(self._on_ingredient_selected)
        # Ingredient name editor
        self.view.editIngredientNameClicked.connect(
            self._on_edit_ingredient_name_clicked
        )
        self.ingredient_name_editor_dialog = EntityNameEditorDialog(
            entity_name="ingredient",
            check_name_available=lambda name: name not in self._ingredient_name_ids.str_values,
        )
        self.ingredient_name_editor_dialog.onNameAccepted.connect(self._on_ingredient_name_accepted)
        # Ingredient description editor
        self.view.ingredientDescriptionChanged.connect(
            self._on_ingredient_description_changed
        )
        # Standard unit editor
        self.standard_unit_editor = StandardUnitEditor(
            get_available_units=lambda: self._global_units,
            view=self.view.standard_unit_editor,
            parent=self.view,
        )
        self.standard_unit_editor.onUnitChanged.connect(
            lambda unit_id: setattr(self.ingredient, 'standard_unit_id', unit_id)
        )
        # Unit conversions editor
        self.unit_conversion_ctrl = UnitConversionsEditor(
            global_units=self._global_units,
            get_existing_conversions=lambda: self.ingredient.unit_conversions,
            check_conversion_available=lambda from_unit_id, to_unit_id: not self._ingredient_unit_system.can_convert_units(
                from_unit_id=from_unit_id,
                to_unit_id=to_unit_id,
            ),
            create_conversion_callback=self._on_unit_conversion_added,
            view=self.view.unit_conversions_editor,
        )
        self.unit_conversion_ctrl.conversionRemoved.connect(self._on_unit_conversion_removed)
        self.unit_conversion_ctrl.conversionUpdated.connect(self._on_unit_conversion_updated)
        # Cost editor
        self.cost_editor_ctrl = CostEditor(
            view=self.view.cost_editor,
            get_available_units=lambda: self._ingredient_unit_system.get_available_units(),
        )
        self.cost_editor_ctrl.costUpdated.connect(self._on_ingredient_cost_changed)
        # Flags editor
        self.flag_editor = FlagEditor(
            global_flags=self._flag_name_ids,
            view=self.view.flag_editor,
            get_entity_flags=lambda: self.ingredient.flags
        )
        self.flag_editor.flagChanged.connect(self._on_flag_changed)
        # Ingredient nutrient editor
        self.ingredient_nutrient_editor_ctrl = NutrientQuantitiesEditor(
            view=self.view.nutrient_quantities_editor,
            global_leaf_nutrients=self._global_leaf_nutrients,
            available_mass_units=self._global_mass_units,
            get_ingredient_nutrient_data=lambda: self.ingredient.nutrient_quantities,
            on_nutrient_qty_changed=self._on_nutrient_qty_changed,
            scale_1g_to_new_unit=lambda new_unit_id: self._ingredient_unit_system.convert_units(
                quantity=1,
                from_unit_id=self._gram_id,
                to_unit_id=new_unit_id,
            ),
        )

        # Connect signals and slots
        self.view.txt_gi.textChanged.connect(self._on_gi_value_changed)

        # Create dialog boxes
        self._ingredient_name_editor_dialog_view = EntityNameEditorDialog(
            parent=self.view,
            check_name_available=lambda name: name not in self._ingredient_name_ids.str_values,
            on_name_accepted_callback=self._on_ingredient_name_accepted,
        )
        self._select_ingredient_name_for_delete_dialog_view: ErrorDialogBoxView
        self._confirm_delete_ingredient_dialog = ConfirmFileDeleteDialog(
            entity_name="Ingredient",
            confirm_delete_callback=self._on_confirm_delete_ingredient_clicked,
        )

        # Load the first ingredient into the view
        self.ingredient = self.db_service.read_ingredient(
            ingredient_id=self._ingredient_name_ids.int_values[0]
        )
        self.load_ingredient(self.ingredient)

    @property
    def ingredient(self) -> Ingredient:
        """Get the ingredient instance."""
        return self._ingredient

    @ingredient.setter
    def ingredient(self, ingredient: Ingredient):
        """Set the ingredient instance."""
        self._ingredient = ingredient

    def load_ingredient(self, ingredient: Ingredient) -> None:
        """Load an ingredient into the editor."""
        self.ingredient = ingredient
        self._ingredient_unit_system.ingredient_unit_conversions = ingredient.unit_conversions
        self.update_view()

    def update_view(self) -> None:
        """Update the view to reflect the state of the current ingredient.
        This is an expensive operation and should be used sparingly.
        """
        # Update the views
        self.view.ingredient_name = self.ingredient.name
        self.view.ingredient_description = self.ingredient.description
        self.standard_unit_editor_ctrl.selected_unit_id = self.ingredient.standard_unit_id
        self.unit_conversion_ctrl.reset_unit_conversions(self.ingredient.unit_conversions) # type: ignore
        self.cost_editor_ctrl.set_cost_info(
            cost_value=self.ingredient.cost_value,
            cost_qty_value=self.ingredient.cost_qty_value,
            cost_qty_unit_id=self.ingredient.cost_qty_unit_id,
        )
        self.flag_editor.set_flags(self.ingredient.flags)
        # Update the GI field
        self.view.update_gi(self.ingredient.gi)
        # Set the nutrients
        self.ingredient_nutrient_editor_ctrl.set_nutrient_quantities(self.ingredient.nutrient_quantities)

    def _on_ingredient_selected(self, ing_name_and_id: Tuple[str, int]) -> None:
        """Handles the user clicking on an ingredient in the search results.
        Args:
            ing_name_and_id (Tuple[str, int]): The name and ID of the selected ingredient.
        Returns:
            None
        """
        ingredient_id = ing_name_and_id[1]
        # Read the ingredient from the database
        ingredient = self.db_service.read_ingredient(ingredient_id=ingredient_id)
        # Load the ingredient into the view
        self.load_ingredient(ingredient)

    def _on_add_new_ingredient_clicked(self) -> None:
        """Handles user clicking the add new ingredient button.
        Shows the dialog to guide the user through adding an ingredient.
        """
        # Open the create new ingredient dialog box
        self.ingredient_name_editor_dialog_view.clear()
        self.ingredient_name_editor_dialog_view.show()

    def _on_delete_ingredient_clicked(self) -> None:
        """Handles user clicking the delete ingredient button.
        If no ingredient is selected, creates an error dialog to tell the user to select one.
        If an ingredient is selected, creates a confirm dialog to confirm deletion.
        """
        # If no ingredient is selected,
        if self.view.ingredient_search.lst_search_results.item_is_selected is False:
            # Show the dialog to tell the user to select it.
            self.select_ingredient_name_for_delete_dialog_view.show()
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
        ingredient_id = self.ingredient_search.selected_item_data
        assert ingredient_id is not None and type(ingredient_id) == int
        # Grab the selected ingredient name from the search widget
        ingredient_name = self.view.ingredient_search.results_list.selected_item.text()  # type: ignore
        # Delete the ingredient from the database
        self.db_service.repository.delete_ingredient(ingredient_id)
        # Recache the ingredient names
        self._cache_ingredient_names()
        # Reset the search pane
        self.ingredient_search.reset_search()

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
    
    def _on_unit_conversion_added(self, from_unit_id: int, to_unit_id) -> tuple[int, int]:
        """Handler for a unit conversion being added to the ingredient.
        Args:
            from_unit_id (int): The ID of the unit to convert from.
            to_unit_id (int): The ID of the unit to convert to.
        Returns:
            tuple[int, int]: The IDs of the new unit conversion, and the ID of the entity.
        """
        # Insert the new unit conversion into the database
        unit_conversion = self.db_service.create_ingredient_unit_conversion(
            ingredient_id=self.ingredient.id,
            from_unit_id=from_unit_id,
            to_unit_id=to_unit_id
        )
        self.db_service.repository.commit()
        # Add the new unit conversion to the ingredient
        self.ingredient.add_unit_conversion(unit_conversion)
        # Return the ID of the new unit conversion
        return unit_conversion.id

    def _on_unit_conversion_removed(self, unit_conversion_id: int) -> None:
        """Handler for a unit conversion being removed from the ingredient.
        Args:
            unit_conversion_id (int): The ID of the unit conversion to remove.
        Returns:
            None
        """
        # Remove the unit conversion from the ingredient
        self.ingredient.remove_unit_conversion(unit_conversion_id)
        # Remove the unit conversion from the database
        self.db_service.repository.delete_ingredient_unit_conversion(unit_conversion_id)
        self.db_service.repository.commit()

    def _on_unit_conversion_updated(self, unit_conversion_id: int, from_unit_qty: float|None, to_unit_qty: float|None) -> None:
        """Handler for a unit conversion being updated.
        Args:
            unit_conversion_id (int): The ID of the unit conversion to update.
            from_unit_qty (float|None): The quantity of the from unit.
            to_unit_qty (float|None): The quantity of the to unit.
        Returns:
            None
        """
        # Fetch the unit conversion from the ingredient
        unit_conversion = self.ingredient.unit_conversions[unit_conversion_id]
        # Update the unit conversion
        unit_conversion.from_unit_qty = from_unit_qty
        unit_conversion.to_unit_qty = to_unit_qty
        # Update the unit conversion in the database
        self.db_service.update_ingredient_unit_conversion(unit_conversion)
        self.db_service.repository.commit()

    def _on_ingredient_cost_changed(
        self,
        cost_value: float | None,
        cost_qty_value: float | None,
        cost_qty_unit_id: int,
    ) -> None:
        """Handler for changes to the ingredient cost.
        Updates the costs on the model and saves changes to the database.
        Args:
            cost_value (float | None): The cost of the ingredient.
            cost_qty_value (float | None): The quantity of the ingredient.
            cost_qty_unit_id (int): The ID of the unit for the cost quantity.
        Returns:
            None
        """
        # Update the ingredient cost on the model
        self.ingredient.cost_value = cost_value
        self.ingredient.cost_qty_value = cost_qty_value
        self.ingredient.cost_qty_unit_id = cost_qty_unit_id
        # Update the ingredient cost in the database
        self.db_service.repository.update_ingredient_cost(
            ingredient_id=self.ingredient.id,
            cost_value=cost_value,
            cost_qty_value=cost_qty_value,
            cost_qty_unit_id=cost_qty_unit_id,
        )
        self.db_service.repository.commit()

    def _on_flag_changed(self, flag_id: int, flag_value: bool|None) -> None:
        """Handler for changes to the ingredient flags."""
        # Update flag on the model
        self.ingredient.set_flag(flag_id, flag_value)
        # Update the flag in the database
        self.db_service.repository.update_ingredient_flag(
            ingredient_id=self.ingredient.id,
            flag_id=flag_id,
            flag_value=flag_value,
        )

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

