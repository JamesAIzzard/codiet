from typing import Callable

from PyQt6.QtCore import pyqtSignal

from codiet.models.units import Unit, UnitConversion
from codiet.views.units import (
    StandardUnitEditorView,
    UnitConversionEditorView,
    UnitConversionsEditorView,
    UnitConversionDefinitionPopupView,
)
from codiet.views.dialog_box_views import EntityNameDialogView, OkDialogBoxView
from codiet.controllers.entity_name_dialog_ctrl import EntityNameDialogCtrl


class StandardUnitEditorCtrl:
    """A controller for the standard unit editor view."""

    def __init__(
        self,
        view: StandardUnitEditorView,
        unit_list: dict[int, Unit],
        on_standard_unit_changed: Callable[[int], None],
    ):
        """Initialise the standard unit editor controller.
        Args:
            view (StandardUnitEditorView): The standard unit editor view.
            unit_list (dict[int, Unit]): A dictionary of units, keyed against their global IDs.
            on_standard_unit_changed (Callable[[int | None], None]): A callback function that is called when the standard unit is changed.
        """
        self.view = view
        self._on_standard_unit_changed = on_standard_unit_changed
        # Initialise the units in the view
        for unit_id, unit in unit_list.items():
            self.view.cmb_standard_unit.add_unit(
                unit_display_name=unit.plural_display_name, unit_global_id=unit_id
            )

    @property
    def selected_unit_id(self) -> int:
        """Return the global ID of the selected unit."""
        return self.view.cmb_standard_unit.selected_unit_id
    
    @selected_unit_id.setter
    def selected_unit_id(self, unit_id: int):
        """Set the selected unit by its global ID."""
        self.view.cmb_standard_unit.selected_unit_id = unit_id

    def on_standard_unit_changed(self, unit_id: int):
        """Called when the standard unit is changed.
        Args:
            unit_id (int): The global ID of the new standard unit.
        """
        self._on_standard_unit_changed(unit_id)


class UnitConversionsEditorCtrl:

    def __init__(
        self,
        view: UnitConversionsEditorView,
        global_units: dict[int, Unit],
        check_conversion_available: Callable[[int, int], bool],
        on_unit_conversion_added: Callable[[int, int], int],
        on_unit_conversion_removed: Callable[[int], None],
        on_unit_conversion_updated: Callable[[int, float|None, float|None], None],
    ):
        """Initialise the unit conversions editor controller.
        Args:
            view (UnitConversionsEditorView): The unit conversions editor view.
            global_units (dict[int, Unit]): A dictionary of global units, keyed against their global IDs.
            check_conversion_available (Callable[[int, int], bool]): A function that checks if a conversion is available.
            on_unit_conversion_added (Callable[[int, int], int]): A callback function that is called when a unit conversion is added.
                Args:
                    from_unit_id (int): The global ID of the from unit.
                    to_unit_id (int): The global ID of the to unit.
                Returns:
                    int: The global ID of the new unit conversion.
            on_unit_conversion_removed (Callable[[int], None]): A callback function that is called when a unit conversion is removed.
            on_unit_conversion_updated (Callable[[int, float, float], None]): A callback function that is called when a unit conversion is updated.
        """
        self.view = view
        self.global_units = global_units
        self._check_conversion_available = check_conversion_available
        self._on_unit_conversion_added_callback = on_unit_conversion_added
        self._on_unit_conversion_removed_callback = on_unit_conversion_removed
        self._on_unit_conversion_updated_callback = on_unit_conversion_updated

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
            from_unit_display_name=self.global_units[unit_conversion.from_unit_id].plural_display_name,
            to_unit_display_name=self.global_units[unit_conversion.to_unit_id].plural_display_name,
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

    def reset_unit_conversions(self, unit_conversions: dict[int, UnitConversion]) -> None:
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
        from_unit_qty: float|None,
        to_unit_qty: float|None,
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


class UnitConversionDefinitionPopupCtrl:
    """Controller for the unit conversion definition popup."""

    def __init__(
        self,
        view: UnitConversionDefinitionPopupView,
        on_unit_conversion_added: Callable[[int, int], None],
        global_units: dict[int, Unit],
        check_conversion_available: Callable[[int, int], bool],
    ):
        """Initialise the unit conversion definition popup controller.
        Args:
            view (UnitConversionDefinitionPopupView): The unit conversion definition popup view.
            on_unit_conversion_added (Callable[[int, int, float, float], None]): A callback function that is called when a unit conversion is added.
            global_units (dict[int, Unit]): A dictionary of global units, keyed against their global IDs.
            check_conversion_available (Callable[[int, int], bool]): A function that checks if a conversion is available.
        """
        self.view = view
        self._on_unit_conversion_added = on_unit_conversion_added
        self._check_conversion_available = check_conversion_available
        # Load the global units into both columns in the view
        for unit_id, unit in global_units.items():
            self.view.from_unit_selector.lst_search_results.add_item(
                item_content=unit.plural_display_name, data=unit_id
            )
            self.view.to_unit_selector.lst_search_results.add_item(
                item_content=unit.plural_display_name, data=unit_id
            )
        # Connect the signals
        self.view.selectionChanged.connect(self._on_selection_changed)
        self.view.btn_ok.clicked.connect(self._on_ok_clicked)
        self.view.btn_cancel.clicked.connect(self.view.close)

    def _on_selection_changed(self, from_unit_id: int, to_unit_id: int) -> None:
        """Called when either of the unit selections are changed.
        Args:
            from_unit_id (int): The global ID of the from unit.
            to_unit_id (int): The global ID of the to unit.
        """
        # Check if the conversion is available
        conversion_available = self._check_conversion_available(
            from_unit_id, to_unit_id
        )
        # Enable the OK button if the conversion is available
        self.view.btn_ok.setEnabled(conversion_available)

    def _on_ok_clicked(self):
        """Called when the OK button is clicked."""
        # Get the from and to unit IDs
        from_unit_id = (
            self.view.from_unit_selector.lst_search_results.selected_item_data
        )
        to_unit_id = self.view.to_unit_selector.lst_search_results.selected_item_data
        # Call the on_unit_conversion_added callback
        self._on_unit_conversion_added(from_unit_id, to_unit_id)
        # Close the view
        self.view.close()
