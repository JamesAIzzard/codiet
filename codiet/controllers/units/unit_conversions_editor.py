from typing import Callable

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject, pyqtSignal, QVariant

from codiet.models.units import Unit
from codiet.views.units.unit_conversions_editor_view import UnitConversionsEditorView


class UnitConversionsEditor(QObject):
    """Controller for the unit conversions editor view.

    Signals:
        onConversionAdded: Emitted when a unit conversion is added.
            Args: unit_conversion_id (int), from_unit_id (int), to_unit_id (int).
        onConversionRemoved: Emitted when a unit conversion is removed.
            Args: unit_conversion_id (int).
        onConversionChanged: Emitted when a unit conversion is changed.
            Args: unit_conversion_id (int), from_unit_id (int), to_unit_id (int),
                       from_unit_qty (QVariant), to_unit_qty (QVariant).
    """

    onConversionAdded = pyqtSignal(int, int)
    onConversionRemoved = pyqtSignal(int)
    onConversionUpdated = pyqtSignal(int, int, int, QVariant, QVariant)

    def __init__(
        self,
        get_existing_conversions: Callable[[], dict[int, UnitConversion]],
        get_available_units: Callable[[], dict[int, Unit]],
        check_conversion_available: Callable[[int, int], bool],
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
        self._get_available_units = get_available_units
        self._check_conversion_available = check_conversion_available

        # Connect the signals
        self.view.addUnitClicked.connect(self._on_add_conversion_clicked)
        self.view.removeUnitClicked.connect(self._on_unit_conversion_removed)
        self.view.flipConversionClicked.connect(self._on_unit_conversion_updated)

        # Init the conversion definition dialog


    def add_unit_conversion(self, unit_conversion: UnitConversion) -> None:
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
            from_unit_display_name=self.global_units[
                unit_conversion.from_unit_id
            ].plural_display_name,
            to_unit_display_name=self.global_units[
                unit_conversion.to_unit_id
            ].plural_display_name,
        )
        # Connect the signals
        view.conversionUpdated.connect(self._on_unit_conversion_updated)
        # Add the unit conversion to the view
        self.view.add_unit_conversion(
            unit_conversion_view=view, unit_conversion_id=unit_conversion.id
        )

    def add_unit_conversions(self, unit_conversions: dict[int, UnitConversion]) -> None:
        """Add multiple unit conversions to the view.
        Args:
            unit_conversions (dict[int, IngredientUnitConversion]): A dictionary of unit conversions, keyed against their global IDs.
        Returns:
            None
        """
        for unit_conversion in unit_conversions.values():
            self.add_unit_conversion(unit_conversion)

    def set_unit_conversions(self, unit_conversions: dict[int, UnitConversion]) -> None:
        """Reset the unit conversions in the view.
        Args:
            unit_conversions (dict[int, IngredientUnitConversion]): A dictionary of unit conversions, keyed against their global IDs.
        Returns:
            None
        """
        self.view.clear_all_unit_conversions()
        self.add_unit_conversions(unit_conversions)

    def _on_add_conversion_clicked(self):
        """Called when the add conversion button is clicked. Opens the popup to help the user
        define a new unit conversion."""
        # Init a unit conversion definition popup
        popup = UnitConversionDefinitionPopupCtrl(
            view=UnitConversionDefinitionPopupView(),
            on_unit_conversion_added=self._on_unit_conversion_added,
            global_units=self.global_units,
            check_conversion_available=self._check_conversion_available,
        )
        # Bind the OK button to the on_unit_conversion_added method
        popup.view.btn_ok.clicked.connect(self._on_unit_conversion_added)
        # Show the unit conversion definition dialog
        popup.view.show()

    def _on_unit_conversion_added(self, from_unit_id: int, to_unit_id: int) -> None:
        """Called when a unit conversion is added.
        Args:
            from_unit_id (int): The global ID of the from unit.
            to_unit_id (int): The global ID of the to unit.
        Returns:
            None
        """
        # Call the callback and collect the ID
        id = self._on_unit_conversion_added_callback(from_unit_id, to_unit_id)
        # Create a unit conversion instance
        unit_conversion = UnitConversion(
            id=id, from_unit_id=from_unit_id, to_unit_id=to_unit_id
        )
        # Add the unit conversion to the view
        self.add_unit_conversion(unit_conversion)

    def _on_unit_conversion_removed(self, unit_conversion_id: int):
        """Called when a unit conversion is removed.
        Args:
            unit_conversion_id (int): The global ID of the unit conversion.
        """
        # Call the callback
        self._on_unit_conversion_removed_callback(unit_conversion_id)

    def _on_unit_conversion_updated(
        self,
        unit_conversion_id: int,
        from_unit_qty: float | None,
        to_unit_qty: float | None,
    ):
        """Called when a unit conversion is updated.
        Args:
            unit_conversion_id (int): The global ID of the unit conversion.
            from_unit_qty (float): The quantity of the from unit.
            to_unit_qty (float): The quantity of the to unit.
        """
        # Call the callback
        self._on_unit_conversion_updated_callback(
            unit_conversion_id, from_unit_qty, to_unit_qty
        )
