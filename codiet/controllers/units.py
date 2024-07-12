from typing import Callable

from PyQt6.QtCore import pyqtSignal

from codiet.models.units import Unit, UnitConversion
from codiet.views.units import (
    StandardUnitEditorView,
    UnitConversionEditorView,
    UnitConversionsEditorView,
    UnitConversionDefinitionPopupView,
)
from codiet.views.dialogs import EntityNameDialogView, OkDialogBoxView
from codiet.controllers.dialogs.entity_name_dialog_ctrl import EntityNameDialog








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
