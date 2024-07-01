from typing import Callable

from PyQt6.QtCore import pyqtSignal

from codiet.models.units import Unit, IngredientUnitConversion
from codiet.views.units import StandardUnitEditorView, UnitConversionsEditorView, UnitConversionDefinitionPopupView
from codiet.views.dialog_box_views import EntityNameDialogView, OkDialogBoxView
from codiet.controllers.entity_name_dialog_ctrl import EntityNameDialogCtrl


class StandardUnitEditorCtrl:
    """A controller for the standard unit editor view."""

    def __init__(
        self,
        view: StandardUnitEditorView,
        unit_list: dict[int, Unit],
        on_standard_unit_changed: Callable[[int], None],
        current_standard_unit_id: int,
    ):
        """Initialise the standard unit editor controller.
        Args:
            view (StandardUnitEditorView): The standard unit editor view.
            unit_list (dict[int, Unit]): A dictionary of units, keyed against their global IDs.
            on_standard_unit_changed (Callable[[int | None], None]): A callback function that is called when the standard unit is changed.
            current_standard_unit_id (int): The global ID of the current standard unit.
        """
        self.view = view
        self._on_standard_unit_changed = on_standard_unit_changed
        # Initialise the units in the view
        for unit_id, unit in unit_list.items():
            self.view.cmb_standard_unit.add_unit(
                unit_display_name=unit.plural_display_name, unit_global_id=unit_id
            )
        # Select the current standard unit
        self.view.cmb_standard_unit.selected_unit_id = current_standard_unit_id


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
        on_unit_conversion_added: Callable[[int, int], None],
        on_unit_conversion_removed: Callable[[int], None],
        on_unit_conversion_updated: Callable[[int, float, float], None],
    ):
        self.view = view
        self.global_units = global_units
        self._check_conversion_available = check_conversion_available
        self._on_unit_conversion_added_callback = on_unit_conversion_added
        self._on_unit_conversion_removed_callback = on_unit_conversion_removed
        self._on_unit_conversion_updated_callback = on_unit_conversion_updated

    def _on_add_conversion_clicked(self):
        """Called when the add conversion button is clicked."""
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

    def _on_unit_conversion_added(self, from_unit_id: int, to_unit_id: int):
        """Called when a unit conversion is added.
        Args:
            from_unit_id (int): The global ID of the from unit.
            to_unit_id (int): The global ID of the to unit.
        """
        # Get the conversion factor and offset
        conversion_factor = self.view.get_conversion_factor()
        offset = self.view.get_offset()
        # Call the on_unit_conversion_added callback
        self._on_unit_conversion_added(from_unit_id, to_unit_id, conversion_factor, offset)

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
        conversion_available = self._check_conversion_available(from_unit_id, to_unit_id)
        # Enable the OK button if the conversion is available
        self.view.btn_ok.setEnabled(conversion_available)

    def _on_ok_clicked(self):
        """Called when the OK button is clicked."""
        # Get the from and to unit IDs
        from_unit_id = self.view.from_unit_selector.lst_search_results.selected_item_data
        to_unit_id = self.view.to_unit_selector.lst_search_results.selected_item_data
        # Call the on_unit_conversion_added callback
        self._on_unit_conversion_added(from_unit_id, to_unit_id)
        # Close the view
        self.view.close()