from copy import deepcopy
from typing import Callable

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject, pyqtSignal

from codiet.model.units.unit import Unit
from codiet.model.units.global_unit_conversion import GlobalUnitConversion
from codiet.model.units.ingredient_unit_conversion import IngredientUnitConversion
from codiet.views.units.unit_conversion_editor_view import UnitConversionEditorView
from codiet.views.units.unit_conversions_editor_view import UnitConversionsEditorView
from codiet.controllers.units.unit_conversion_definition_dialog import UnitConversionDefinitionDialog


class UnitConversionsEditor(QObject):
    """Module to manage unit conversions associated with an entity.

    Signals:
        conversionAdded (object): Emitted when a unit conversion is added.
            object: The unit conversion object.
        conversionRemoved (int): Emitted when a unit conversion is removed.
            int: The global ID of the unit conversion.
        conversionUpdated (object): Emitted when a unit conversion is updated.
            object: The unit conversion object.
    """

    conversionAdded = pyqtSignal(object)
    conversionUpdated = pyqtSignal(object)
    conversionRemoved = pyqtSignal(int)

    def __init__(
        self,
        get_global_units: Callable[[], dict[int, Unit]],
        get_global_unit_conversions: Callable[[], dict[int, GlobalUnitConversion]],
        get_entity_unit_conversions: Callable[[], dict[int, IngredientUnitConversion]],
        view: UnitConversionsEditorView | None = None,
        parent: QWidget | None = None,
    ):
        """Initialise the unit conversions editor controller."""
        super().__init__()

        # Build the view if it is not provided
        if view is None:
            view = UnitConversionsEditorView(parent=parent)
        self.view = view

        # Stash the parameters
        self._get_global_units = get_global_units
        self._get_global_unit_conversions = get_global_unit_conversions
        self._get_entity_unit_conversions = get_entity_unit_conversions

        # Connect the signals
        self.view.btn_add.clicked.connect(self._on_add_conversion_clicked)
        self.view.removeUnitClicked.connect(self.conversionRemoved.emit)
        self.view.flipConversionClicked.connect(self._on_unit_conversion_updated)

        # Init and connect the conversion definition dialog
        self.conversion_definition_dialog = UnitConversionDefinitionDialog(
            get_global_units=lambda: self._get_global_units(),
            check_conversion_available=self._check_conversion_available,
            parent=self.view
        )
        self.conversion_definition_dialog.conversionCreated.connect(
            self._on_unit_conversion_added
        )

        # Populate the view with the current unit conversions
        self.refresh()


    def refresh(self) -> None:
        """Refresh the module with the current unit conversions."""
        # Clear the existing unit conversions
        self.view.conversion_list.clear()
        # Add the new unit conversions
        for unit_conversion in self._get_entity_unit_conversions().values():
            self._add_unit_conversion(unit_conversion)

    def _add_unit_conversion(self, unit_conversion: IngredientUnitConversion) -> None:
        """Add a unit conversion.
        Args:
            unit_conversion (IngredientUnitConversion): The unit conversion to add.
        Returns:
            None
        """
        # Create the new unit conversion editor view
        view = UnitConversionEditorView(
            id=unit_conversion.id,
            from_unit_id=unit_conversion.from_unit_id,
            to_unit_id=unit_conversion.to_unit_id,
            from_unit_display_name=self._get_global_units()[
                unit_conversion.from_unit_id
            ]._plural_display_name,
            to_unit_display_name=self._get_global_units()[
                unit_conversion.to_unit_id
            ]._plural_display_name,
        )
        # Connect the signals
        view.conversionUpdated.connect(self._on_unit_conversion_updated)
        # Add the unit conversion to the view
        self.view.conversion_list.add_item_content(
            item_content=view, 
            data=unit_conversion.id
        )

    def _check_conversion_available(self, from_unit_id: int, to_unit_id: int) -> bool:
        """Check if a conversion is available between two units.
        Args:
            from_unit_id (int): The global ID of the from unit.
            to_unit_id (int): The global ID of the to unit.
        Returns:
            bool: True if the conversion is available, False otherwise.
        """
        # Concatenate the global and entity unit conversions
        all_unit_conversions = {
            **self._get_global_unit_conversions(),
            **self._get_entity_unit_conversions(),
        }
        # Check if the conversion already exists
        for conversion in all_unit_conversions.values():
            # Check one way
            if (
                conversion.from_unit_id == from_unit_id
                and conversion.to_unit_id == to_unit_id
            ):
                return False
            # Check the other way
            if (
                conversion.from_unit_id == to_unit_id
                and conversion.to_unit_id == from_unit_id
            ):
                return False
        return True

    def _on_add_conversion_clicked(self):
        """Called when the add conversion button is clicked. Opens the popup to help the user
        define a new unit conversion."""
        # Show the conversion definition dialog
        self.conversion_definition_dialog.view.show()

    def _on_unit_conversion_added(self, from_unit_id: int, to_unit_id: int) -> None:
        """Called when a unit conversion is added.
        Args:
            from_unit_id (int): The global ID of the from unit.
            to_unit_id (int): The global ID of the to unit.
        Returns:
            None
        """
        # Create a unit conversion instance
        conversion = IngredientUnitConversion(
            from_unit_id=from_unit_id,
            to_unit_id=to_unit_id,
            from_unit_qty=None,
            to_unit_qty=None,
        )
        # Emit the signal
        self.conversionAdded.emit(conversion)
        # Refresh the view
        self.refresh()

    def _on_unit_conversion_removed(self, unit_conversion_id: int):
        """Called when a unit conversion is removed.
        Args:
            unit_conversion_id (int): The global ID of the unit conversion.
        """
        # Remove the conversion from the view
        self.view.conversion_list.remove_item(data=unit_conversion_id)
        # Emit the signal
        self.conversionRemoved.emit(unit_conversion_id)

    def _on_unit_conversion_updated(
        self,
        unit_conversion_id: int,
        from_unit_id: int,
        to_unit_id: int,
        from_unit_qty: float | None,
        to_unit_qty: float | None,
    ):
        """Called when a unit conversion is updated.
        Args:
            unit_conversion_id (int): The global ID of the unit conversion.
            from_unit_qty (float): The quantity of the from unit.
            to_unit_qty (float): The quantity of the to unit.
        """
        # Grab the conversion object
        conversion = self._get_entity_unit_conversions()[unit_conversion_id]
        # Copy it to avoid mutating the original
        conversion = deepcopy(conversion)
        # Update the conversion object
        conversion.from_unit_id = from_unit_id
        conversion.to_unit_id = to_unit_id
        conversion.from_unit_qty = from_unit_qty
        conversion.to_unit_qty = to_unit_qty
        # Emit the signal
        self.conversionUpdated.emit(conversion)
