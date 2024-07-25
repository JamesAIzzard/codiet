from typing import Tuple

from PyQt6.QtWidgets import QWidget

from codiet.db.database_service import DatabaseService

from codiet.models.ingredients.ingredient import Ingredient
from codiet.models.nutrients import filter_leaf_nutrients
from codiet.models.nutrients.entity_nutrient_quantity import EntityNutrientQuantity
from codiet.models.units.entity_unit_conversion import EntityUnitConversion
from codiet.models.units.entity_units_system import EntityUnitsSystem
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.controllers.search.search_column import SearchColumn
from codiet.controllers.dialogs.entity_name_editor_dialog import EntityNameEditorDialog
from codiet.controllers.units.standard_unit_editor import StandardUnitEditor
from codiet.controllers.units.unit_conversions_editor import UnitConversionsEditor
from codiet.controllers.cost_editor import CostEditor
from codiet.controllers.flags.flag_editor import FlagEditor
from codiet.controllers.nutrients.nutrient_quantities_editor import NutrientQuantitiesEditor


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
        self._global_flags = self.db_service.repository.read_all_global_flags()
        self._flag_name_ids = self.db_service.build_flag_name_id_map()
        self._global_nutrients = self.db_service.read_all_global_nutrients()
        self._global_leaf_nutrients = filter_leaf_nutrients(self._global_nutrients)
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
            get_searchable_strings=lambda: self._ingredient_name_ids.values,
        )
        self.ingredient_search_column.onResultSelected.connect(self._on_ingredient_selected)
        # Ingredient name editor
        self.view.editIngredientNameClicked.connect(
            self._on_edit_ingredient_name_clicked
        )
        self.ingredient_name_editor_dialog = EntityNameEditorDialog(
            entity_name="ingredient",
            check_name_available=lambda name: name not in self._ingredient_name_ids.values,
        )
        self.ingredient_name_editor_dialog.onNameAccepted.connect(self._on_ingredient_name_accepted)
        # Ingredient description editor
        self.view.ingredientDescriptionChanged.connect(
            self._on_ingredient_description_changed
        )
        # Standard unit editor
        self.standard_unit_editor = StandardUnitEditor(
            get_available_units=lambda: self._ingredient_unit_system.available_units,
            view=self.view.standard_unit_editor,
            parent=self.view,
        )
        self.standard_unit_editor.onUnitChanged.connect(
            lambda unit_id: setattr(self.ingredient, 'standard_unit_id', unit_id)
        )
        # Unit conversions editor
        self.unit_conversion_editor = UnitConversionsEditor(
            get_global_units=lambda: self._global_units,
            get_global_unit_conversions=lambda: self._global_unit_conversions,
            get_entity_unit_conversions=lambda: self.ingredient.unit_conversions,
            view=self.view.unit_conversions_editor,
        )
        self.unit_conversion_editor.conversionAdded.connect(self._on_unit_conversion_added)
        self.unit_conversion_editor.conversionRemoved.connect(self._on_unit_conversion_removed)
        self.unit_conversion_editor.conversionUpdated.connect(self._on_unit_conversion_updated)
        # Cost editor
        self.cost_editor = CostEditor(
            view=self.view.cost_editor,
            get_available_units=lambda: self._ingredient_unit_system.get_available_units_from_root(),
            get_cost_data=lambda: (
                self.ingredient.cost_value,
                self.ingredient.cost_qty_value,
                self.ingredient.cost_qty_unit_id,
            ),
        )
        self.cost_editor.costUpdated.connect(self._on_ingredient_cost_changed)
        # Flags editor
        self.flag_editor = FlagEditor(
            get_global_flags=lambda: self._global_flags,
            get_entity_flags=lambda: self.ingredient.flags,
            view=self.view.flag_editor
        )
        self.flag_editor.flagChanged.connect(self._on_flag_changed)
        # GI editor
        self.view.txt_gi.textChanged.connect(self._on_gi_value_changed)        
        # Ingredient nutrient editor
        self.nutrient_quantities_editor = NutrientQuantitiesEditor(
            view=self.view.nutrient_quantities_editor,
            get_global_leaf_nutrients=lambda: self._global_leaf_nutrients,
            get_global_mass_units=lambda: self._global_mass_units,
            get_entity_available_units=lambda: self._ingredient_unit_system.available_units,
            get_entity_nutrient_quantities=lambda: self.ingredient.nutrient_quantities,
            rescale_nutrient_mass=self._ingredient_unit_system.rescale_quantity,
            default_mass_unit_id=self._gram_id,
        )
        self.nutrient_quantities_editor.nutrientQuantityAdded.connect(
            self._on_nutrient_qty_added
        )
        self.nutrient_quantities_editor.nutrientQuantityChanged.connect(
            self._on_nutrient_qty_changed
        )
        self.nutrient_quantities_editor.nutrientQuantityRemoved.connect(
            self._on_nutrient_qty_removed
        )

        # Create some other supporting dialogs
        # TODO: Update these to use the new dialog system
        self.error_dialog = ErrorDialog(parent=self.view)
        self.confirm_dialog = ConfirmDialogBoxView(parent=self.view)

        # Load the first ingredient
        # Fetch it first
        first_ingredient = self.db_service.read_ingredient(
            ingredient_id=self._ingredient_name_ids.keys[0]
        )
        # Load it
        self.load_ingredient(first_ingredient)

    @property
    def ingredient(self) -> Ingredient:
        """Get the ingredient instance.
        To set the ingredient, use the load_ingredient method.
        """
        return self._ingredient

    def load_ingredient(self, ingredient: Ingredient) -> None:
        """
        Load an ingredient into the editor and update all views and sub-modules.
        This method should be called whenever a new ingredient is selected or created.
        """
        # Set the ingredient instance
        self._ingredient = ingredient

        # Update the ingredient unit system
        self._ingredient_unit_system.entity_unit_conversions = ingredient.unit_conversions

        # Update main view elements
        self.view.ingredient_name = ingredient.name
        self.view.ingredient_description = ingredient.description
        self.view.gi = ingredient.gi

        # Update sub-modules
        self.standard_unit_editor.selected_unit = ingredient.standard_unit_id
        self.unit_conversion_editor.refresh()
        self.cost_editor.refresh()
        self.flag_editor.refresh()
        self.nutrient_quantities_editor.refresh()

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
        self.ingredient_name_editor_dialog.view.clear()
        self.ingredient_name_editor_dialog.view.show()

    def _on_delete_ingredient_clicked(self) -> None:
        """Handles user clicking the delete ingredient button.
        If no ingredient is selected, creates an error dialog to tell the user to select one.
        If an ingredient is selected, creates a confirm dialog to confirm deletion.
        """
        # If no ingredient is selected,
        if self.view.ingredient_search.search_results.item_is_selected is False:
            # Show the dialog to tell the user to select it.
            self.error_dialog.title = "No Ingredient Selected"
            self.error_dialog.message = "Please select an ingredient to delete."
            self.error_dialog.show()
        else:
            # Show the confirm dialog to confirm deletion
            self.confirm_dialog.title = "Delete Ingredient?"
            self.confirm_dialog.message = (
                f"Are you sure you want to delete {self.view.ingredient_search.search_results.selected_item.text()}?" # type: ignore
            )
            self.confirm_dialog.on_accept_action = self._on_confirm_delete_ingredient_clicked
            self.confirm_dialog.show()

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
    
    def _on_unit_conversion_added(self, unit_conversion: EntityUnitConversion) -> None:
        """Handler for a unit conversion being added to the ingredient.
        Args:
            unit_conversion (EntityUnitConversion): The unit conversion to add.
                id and entity_id are not set.
        Returns:
            EntityUnitConversion: The new unit conversion, with the ID, and from/to unit quantities set.
        """
        # Populate the unit conversion with the ingredient ID
        unit_conversion.entity_id = self.ingredient.id
        # Insert the new unit conversion into the database
        unit_conversion = self.db_service.create_ingredient_unit_conversion(unit_conversion)
        self.db_service.repository.commit()
        # Add the new unit conversion to the ingredient
        self.ingredient.add_unit_conversion(unit_conversion)

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

    def _on_gi_value_changed(self, value: float | None):
        """Handler for changes to the ingredient GI value."""
        # Update the GI value on the model
        self.ingredient.gi = value
        # Update the GI value on the database
        self.db_service.repository.update_ingredient_gi(
            ingredient_id=self.ingredient.id,
            gi=value,
        )
        self.db_service.repository.commit()

    def _on_nutrient_qty_added(self, nutrient_quantity: EntityNutrientQuantity) -> None:
        """Handler for adding a nutrient quantity to the ingredient."""
        # Add the ingredient ID to the nutrient quantity
        nutrient_quantity.parent_entity_id = self.ingredient.id
        # Add the nutrient quantity to the ingredient
        self.ingredient.add_nutrient_quantity(nutrient_quantity)
        # Add the nutrient quantity to the database
        self.db_service.create_ingredient_nutrient_quantity(nutrient_quantity)
        self.db_service.repository.commit()

    def _on_nutrient_qty_changed(self, nutrient_quantity: EntityNutrientQuantity):
        """Handler for changes to the ingredient nutrient quantities."""
        # Update the nutrient quantity on the model
        self.ingredient.update_nutrient_quantity(nutrient_quantity)
        # Update the nutrient quantity in the database
        self.db_service.update_ingredient_nutrient_quantity(nutrient_quantity)

    def _on_nutrient_qty_removed(self, nutrient_id: int):
        """Handler for removing a nutrient quantity from the ingredient."""
        # Raise an exception if the nutrient is not in the ingredient
        if nutrient_id not in self.ingredient.nutrient_quantities:
            raise KeyError(f"Nutrient ID '{nutrient_id}' not in ingredient.")
        # Remove the nutrient quantity from the ingredient
        self.ingredient.remove_nutrient_quantity(nutrient_id)
        # Remove the nutrient quantity from the database
        self.db_service.repository.delete_ingredient_nutrient_quantity(
            ingredient_id=self.ingredient.id,
            global_nutrient_id=nutrient_id
        )
        self.db_service.repository.commit()

    def _connect_toolbar(self) -> None:
        """Connect the toolbar button signals."""
        self.view.addIngredientClicked.connect(self._on_add_new_ingredient_clicked)
        self.view.deleteIngredientClicked.connect(self._on_delete_ingredient_clicked)
        self.view.autopopulateClicked.connect(self._on_autopopulate_ingredient_clicked)

