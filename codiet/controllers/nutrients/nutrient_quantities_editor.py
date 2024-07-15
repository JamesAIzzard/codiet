from typing import Callable

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget

from codiet.utils.map import IntStrMap
from codiet.models.nutrients import filter_leaf_nutrients
from codiet.models.nutrients.nutrient import Nutrient
from codiet.models.nutrients.entity_nutrient_quantity import EntityNutrientQuantity
from codiet.models.units.unit import Unit
from codiet.models.units.entity_units_system import EntityUnitsSystem
from codiet.views.nutrients.nutrient_quantity_editor_view import NutrientQuantityEditorView
from codiet.views.nutrients.nutrient_quantities_editor_view import NutrientQuantitiesEditorView
from codiet.controllers.search.search_column import SearchColumn


class NutrientQuantitiesEditor(QObject):
    """
    Controller class for managing the editing of nutrient quantities.

    Signals:
        nutrientQuantityAdded (int): Signal emitted when a nutrient quantity is added.
            int: The nutrient global ID.
        nutrientQuantityRemoved (int): Signal emitted when a nutrient quantity is removed.
            int: The nutrient global ID.
        nutrientQuantityChanged (int, int, float, float): Signal emitted when a nutrient quantity is changed.
            int: The nutrient global ID.
            int: The nutrient mass unit ID.
            float: The nutrient mass value.
            float: The ingredient grams value.

    """

    nutrientQuantityAdded = pyqtSignal(object)
    nutrientQuantityRemoved = pyqtSignal(object)
    nutrientQuantityChanged = pyqtSignal(object)

    def __init__(
        self,
        global_nutrients: dict[int, Nutrient],
        global_units: dict[int, Unit],
        entity_unit_system: EntityUnitsSystem,
        get_entity_nutrient_data: Callable[[], dict[int, EntityNutrientQuantity]],
        view: NutrientQuantitiesEditorView|None = None,
        parent: QWidget|None = None
    ) -> None:
        """Initialise the NutrientQuantitiesEditor.

        Args:
            view (NutrientQuantitiesEditorView): The view associated with the editor.
            global_nutrients (dict[int, Nutrient]): A dictionary of global nutrients.
            global_units (dict[int, Unit]): A dictionary of global units.
            entity_unit_system (EntityUnitsSystem): The unit system for the entity.
            get_entity_nutrient_data (Callable[[], dict[int, EntityNutrientQuantity]]): A function to get the entity's nutrient data.

        """
        # Build the view if not provided
        if view is None:
            view = NutrientQuantitiesEditorView(parent=parent)
        self.view = view

        # Stash the callable arguments
        self._global_units = global_units
        self._global_nutrients = global_nutrients
        self._entity_unit_system = entity_unit_system
        self._get_entity_nutrient_data = get_entity_nutrient_data

        # Create a list of just leaf nutrients
        self._leaf_nutrients = filter_leaf_nutrients(global_nutrients)
        # Create a map of leaf nutrient id's to their names
        self._leaf_nutrient_name_id_map = IntStrMap()
        for nutrient_id, nutrient in self._leaf_nutrients.items():
            self._leaf_nutrient_name_id_map.add_mapping(nutrient_id, nutrient.nutrient_name)

        # Init the search column controller in the view
        self.nutrient_quantities_column = SearchColumn(
            get_searchable_strings=lambda: self._leaf_nutrient_name_id_map.str_values,
            get_view_item_and_data_for_string=self._get_nutrient_quantity_view_and_id,
            view=self.view.nutrient_quantities_column,
        )

        # Connect the signals up
        self.view.addNutrientClicked.connect(self._on_add_nutrient_clicked)
        self.view.removeNutrientClicked.connect(self._on_remove_nutrient_clicked)
    
    def _on_add_nutrient_clicked(self) -> None:
        """Handler for when the add nutrient button is clicked."""
        # Open the AddEntityDialog
        raise NotImplementedError

    def _on_remove_nutrient_clicked(self) -> None:
        """Handler for when the remove nutrient button is clicked."""
        # Grab the ID of the selected nutrient
        selected_nutrient_id = self.nutrient_quantities_column.view.search_results.selected_item_data
        if selected_nutrient_id is not None:
            # Remove the nutrient from the listbox
            self.nutrient_quantities_column.view.search_results.remove_selected_item()
            # Emit the nutrientQuantityRemoved signal
            self.nutrientQuantityRemoved.emit(selected_nutrient_id)

    def _get_nutrient_quantity_view_and_id(self, nutrient_name:str) -> tuple[NutrientQuantityEditorView, int]:
        """Generates the nutrient quantity view and ID from the nutrient name.

        Args:
            nutrient_name (str): The name of the nutrient.

        Returns:
            tuple[NutrientQuantityEditorView, int]: The nutrient quantity view and the nutrient global ID.
        """
        # Get the global nutrient ID from the name
        nutrient_id = self._leaf_nutrient_name_id_map.get_int(nutrient_name)
        # Create a new NutrientQuantityEditorView
        nutrient_quantity_view = NutrientQuantityEditorView(
            global_nutrient_id=nutrient_id,
            nutrient_name=nutrient_name
        )
        return nutrient_quantity_view, nutrient_id


