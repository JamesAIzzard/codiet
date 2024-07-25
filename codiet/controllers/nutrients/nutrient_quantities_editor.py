from copy import deepcopy
from typing import Callable

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget

from codiet.utils.bidirectional_map import BidirectionalMap
from codiet.models.nutrients.nutrient import Nutrient
from codiet.models.nutrients.entity_nutrient_quantity import EntityNutrientQuantity
from codiet.models.units.unit import Unit
from codiet.models.units.entity_units_system import EntityUnitsSystem
from codiet.views.nutrients.nutrient_quantity_editor_view import (
    NutrientQuantityEditorView,
)
from codiet.views.nutrients.nutrient_quantities_editor_view import (
    NutrientQuantitiesEditorView,
)
from codiet.controllers.search.search_column import SearchColumn
from codiet.controllers.dialogs.add_entity_dialog import AddEntityDialog


class NutrientQuantitiesEditor(QObject):
    """
    Controller class for the managing the nutrient quantities associated with an entity.

    Signals:
        nutrientQuantityAdded (EntityNutrientQuantity).
        nutrientQuantityRemoved (int).
        nutrientQuantityChanged (EntityNutrientQuantity).
    """

    nutrientQuantityAdded = pyqtSignal(object)
    nutrientQuantityRemoved = pyqtSignal(int)
    nutrientQuantityChanged = pyqtSignal(object)

    def __init__(
        self,
        get_global_leaf_nutrients: Callable[[], dict[int, Nutrient]],
        get_global_mass_units: Callable[[], dict[int, Unit]],
        get_entity_available_units: Callable[[], dict[int, Unit]],
        get_entity_nutrient_quantities: Callable[[], dict[int, EntityNutrientQuantity]],
        rescale_nutrient_mass: Callable[[int, int, float, float, float], float],
        default_mass_unit_id: int,
        view: NutrientQuantitiesEditorView | None = None,
        parent: QWidget | None = None,
    ) -> None:
        """Initialise the NutrientQuantitiesEditor.

        Args:
            get_global_leaf_nutrients (Callable[[], dict[int, Nutrient]]): A callable that returns the global leaf nutrients.
            get_global_mass_units (Callable[[], dict[int, Unit]]): A callable that returns the global mass units.
            get_entity_available_units (Callable[[], dict[int, Unit]]): A callable that returns the available units.
            get_entity_nutrient_quantities (Callable[[], dict[int, EntityNutrientQuantity]]): A callable that returns the entity nutrient quantities.
            rescale_nutrient_mass (Callable[[int, int, float, float, float], float]): A callable that rescales the nutrient mass.
            view (NutrientQuantitiesEditorView, optional): The view to use. Defaults to None.
            parent (QWidget, optional): The parent widget. Defaults to None.

        """
        # Build the view if not provided
        if view is None:
            view = NutrientQuantitiesEditorView(parent=parent)
        self.view = view

        # Stash the constructor arguments
        self._get_global_leaf_nutrients = get_global_leaf_nutrients
        self._get_global_mass_units = get_global_mass_units
        self._get_entity_available_units = get_entity_available_units
        self._get_entity_nutrient_quantities = get_entity_nutrient_quantities
        self._rescale_nutrient_mass = rescale_nutrient_mass
        self._default_mass_unit_id = default_mass_unit_id

        # Cache some values that don't often change
        self._cached_leaf_nutrients = get_global_leaf_nutrients()
        self._cached_mass_units = get_global_mass_units()
        self._cached_leaf_nutrient_name_id_map = BidirectionalMap[int, str]()
        for nutrient_id, nutrient in self._cached_leaf_nutrients.items():
            self._cached_leaf_nutrient_name_id_map.add_mapping(nutrient_id, nutrient.nutrient_name)

        # Init the controller for the view search column
        self.nutrient_quantities_column = SearchColumn(
            get_searchable_strings=lambda: self._cached_leaf_nutrient_name_id_map.values,
            get_view_item_and_data_for_string=self._get_nutrient_quantity_view_and_id,
            view=self.view.nutrient_quantities_column,
        )

        # Init the dialog to add nutrients
        self._add_nutrient_quantity_dialog = AddEntityDialog(
            get_entity_list=lambda: self._cached_leaf_nutrient_name_id_map,
            can_add_entity=lambda nutrient_id: nutrient_id not in self._get_entity_nutrient_quantities().keys(),
            parent=self.view
        )
        self._add_nutrient_quantity_dialog.entityAdded.connect(self._on_nutrient_quantity_added)

        # Connect the signals up
        self.view.addNutrientClicked.connect(self._on_add_nutrient_clicked)
        self.view.removeNutrientClicked.connect(self._on_remove_nutrient_clicked)
    
    def refresh(self) -> None:
        """Refreshes the view."""
        # Clear the nutrient quantities listbox
        self.nutrient_quantities_column.view.search_results.clear()
        # Add the nutrient quantities to the listbox
        for nutrient_quantity in self._get_entity_nutrient_quantities().values():
            self._add_nutrient_quantity(nutrient_quantity)

    def _on_add_nutrient_clicked(self) -> None:
        """Handler for when the add nutrient button is clicked."""
        # Open the AddEntityDialog
        self._add_nutrient_quantity_dialog.view.show()

    def _on_nutrient_quantity_added(self, nutrient_id: int) -> None:
        """Handler for when the user has selected a nutrient from the
        add nutrient dialog. Adds the new nutrient quantity to the listbox.

        Args:
            nutrient_id (int): The global nutrient ID.
        """
        # Create a new EntityNutrientQuantity object
        entity_nutrient_quantity = EntityNutrientQuantity(
            nutrient_id=nutrient_id,
            ntr_mass_unit_id=self._default_mass_unit_id,
        )

        # Get the new nutrient quantity view and id
        nutrient_quantity_view, _ = self._get_nutrient_quantity_view_and_id(
            nutrient_name=self._cached_leaf_nutrient_name_id_map.get_value(nutrient_id)
        )

        # Add the new nutrient quantity to the listbox
        self.nutrient_quantities_column.view.search_results.add_item_content(
            item_content=nutrient_quantity_view, data=nutrient_id
        )

        # Connect the mass and units changed signals.
        nutrient_quantity_view.nutrientMassChanged.connect(self._on_nutrient_mass_changed)
        nutrient_quantity_view.nutrientMassUnitsChanged.connect(self._on_nutrient_mass_units_changed)

        # Emit the nutrientQuantityAdded signal
        self.nutrientQuantityAdded.emit(entity_nutrient_quantity)

    def _add_nutrient_quantity(self, nutrient_quantity: EntityNutrientQuantity) -> None:
        """Adds a nutrient quantity to the listbox.

        Args:
            nutrient_quantity (EntityNutrientQuantity): The nutrient quantity to add.
        """
        # Get the nutrient name
        nutrient_name = self._cached_leaf_nutrient_name_id_map.get_value(nutrient_quantity.nutrient_id)
        # Get the nutrient quantity view
        nutrient_quantity_view, _ = self._get_nutrient_quantity_view_and_id(nutrient_name)
        # Add the nutrient quantity to the listbox
        self.nutrient_quantities_column.view.search_results.add_item_content(
            item_content=nutrient_quantity_view, data=nutrient_quantity.nutrient_id
        )
        # Set the current values on the view
        nutrient_quantity_view.nutrient_mass_value = nutrient_quantity.nutrient_mass_value
        nutrient_quantity_view.nutrient_mass_unit_id = nutrient_quantity.nutrient_mass_unit_id

    def _get_nutrient_quantity_view_and_id(
        self, nutrient_name: str
    ) -> tuple[NutrientQuantityEditorView, int]:
        """Generates the nutrient quantity view and ID from the nutrient name.

        Args:
            nutrient_name (str): The name of the nutrient.

        Returns:
            tuple[NutrientQuantityEditorView, int]: The nutrient quantity view and the nutrient global ID.
        """
        # Get the global nutrient ID from the name
        nutrient_id = self._cached_leaf_nutrient_name_id_map.get_key(nutrient_name)
        if nutrient_id is None:
            raise ValueError(f"Could not find nutrient ID for nutrient name: {nutrient_name}")
        # Create a new NutrientQuantityEditorView
        nutrient_quantity_view = NutrientQuantityEditorView(
            global_nutrient_id=nutrient_id,
            nutrient_name=nutrient_name,
            nutrient_mass_unit_id=self._default_mass_unit_id
        )
        return nutrient_quantity_view, nutrient_id

    def _on_remove_nutrient_clicked(self) -> None:
        """Handler for when the remove nutrient button is clicked."""
        # Grab the ID of the selected nutrient
        selected_nutrient_id = (
            self.nutrient_quantities_column.view.search_results.selected_item_data
        )
        if selected_nutrient_id is not None:
            # Remove the nutrient from the listbox
            self.nutrient_quantities_column.view.search_results.remove_selected_item()
            # Emit the nutrientQuantityRemoved signal
            self.nutrientQuantityRemoved.emit(selected_nutrient_id)

    def _on_nutrient_mass_changed(self, nutrient_id: int, nutrient_mass: float|None) -> None:
        """Handler for when the mass of a nutrient is changed.

        Args:
            nutrient_id (int): The global nutrient ID.
            nutrient_mass (float|None): The new mass value.
        """
        # Grab the corresponding object. Take a copy so we don't mutate the original.
        nutrient_quantity = deepcopy(self._get_entity_nutrient_quantities()[nutrient_id])
        # Update the mass value
        nutrient_quantity.nutrient_mass_value = nutrient_mass
        # Emit the nutrientQuantityChanged signal
        self.nutrientQuantityChanged.emit(nutrient_quantity)

    def _on_nutrient_mass_units_changed(self, nutrient_id: int, unit_id: int) -> None:
        """Handler for when the mass units of a nutrient are changed.

        Args:
            nutrient_id (int): The global nutrient ID.
            unit_id (int): The new unit ID.
        """
        # Grab the corresponding object. Take a copy so we don't mutate the original.
        entity_nutrient_quantity = deepcopy(self._get_entity_nutrient_quantities()[nutrient_id])
        # Update the mass unit
        entity_nutrient_quantity.nutrient_mass_unit_id = unit_id
        # Emit the nutrientQuantityChanged signal
        self.nutrientQuantityChanged.emit(entity_nutrient_quantity)
