from typing import Callable

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject, pyqtSignal

from codiet.models.units.unit import Unit
from codiet.models.units.entity_unit_conversion import EntityUnitConversion
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
        global_units: dict[int, Unit],
        get_existing_conversions: Callable[[], dict[int, EntityUnitConversion]],
        check_conversion_available: Callable[[int, int], bool],
        create_conversion_callback: Callable[[int, int], EntityUnitConversion],
        view: UnitConversionsEditorView | None = None,
        parent: QWidget | None = None,
    ):
        """Initialise the unit conversions editor controller."""
        super().__init__()

        # Build the view if it is not provided
        if view is None:
            view = UnitConversionsEditorView(parent=parent)
        self.view = view

        # Stash the callbacks
        self._global_units = global_units
        self._get_existing_conversions = get_existing_conversions
        self._check_conversion_available = check_conversion_available
        self._create_conversion_callback = create_conversion_callback

        # Connect the signals
        self.view.addUnitClicked.connect(self._on_add_conversion_clicked)
        self.view.removeUnitClicked.connect(self.conversionRemoved.emit)
        self.view.flipConversionClicked.connect(self._on_unit_conversion_updated)

        # Init and connect the conversion definition dialog
        self.conversion_definition_dialog = UnitConversionDefinitionDialog(
            global_units=self._global_units,
            check_conversion_available=self._check_conversion_available,
            parent=self.view
        )
        self.conversion_definition_dialog.conversionCreated.connect(
            self._on_unit_conversion_added
        )


    def add_unit_conversion_to_view(self, unit_conversion: EntityUnitConversion) -> None:
        """Add a unit conversion to the view.
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
            from_unit_display_name=self._global_units[
                unit_conversion.from_unit_id
            ].plural_display_name,
            to_unit_display_name=self._global_units[
                unit_conversion.to_unit_id
            ].plural_display_name,
        )
        # Connect the signals
        view.conversionUpdated.connect(self._on_unit_conversion_updated)
        # Add the unit conversion to the view
        self.view.conversion_list.add_item_content(
            item_content=view, 
            data=unit_conversion.id
        )

    def add_unit_conversions(self, unit_conversions: dict[int, EntityUnitConversion]) -> None:
        """Add multiple unit conversions to the view.
        Args:
            unit_conversions (dict[int, IngredientUnitConversion]): A dictionary of unit conversions, keyed against their global IDs.
        Returns:
            None
        """
        for unit_conversion in unit_conversions.values():
            self.add_unit_conversion_to_view(unit_conversion)

    def set_unit_conversions(self, unit_conversions: dict[int, EntityUnitConversion]) -> None:
        """Sets the unit conversions in the view.

        Removes all existing conversions and replaces them with the new ones.

        Args:
            unit_conversions (dict[int, IngredientUnitConversion]): A dictionary of unit conversions, keyed against their global IDs.
        Returns:
            None
        """
        self.view.conversion_list.clear()
        self.add_unit_conversions(unit_conversions)

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
        # Call the callback and collect the ID
        conversion = self._create_conversion_callback(from_unit_id, to_unit_id)
        # Add the unit conversion to the view
        self.add_unit_conversion_to_view(conversion)
        # Emit the signal
        self.conversionAdded.emit(conversion)

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
        conversion = self._get_existing_conversions()[unit_conversion_id]
        # Update the conversion object
        conversion.from_unit_id = from_unit_id
        conversion.to_unit_id = to_unit_id
        conversion.from_unit_qty = from_unit_qty
        conversion.to_unit_qty = to_unit_qty
        # Emit the signal
        self.conversionUpdated.emit(conversion)
