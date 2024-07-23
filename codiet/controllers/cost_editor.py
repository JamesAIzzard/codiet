from typing import Callable

from PyQt6.QtCore import pyqtSignal, QVariant, QObject
from PyQt6.QtWidgets import QWidget

from codiet.models.units.unit import Unit
from codiet.views.cost_editor_view import CostEditorView


class CostEditor(QObject):
    """Controller for the cost editor widget."""

    costUpdated = pyqtSignal(QVariant, QVariant, int)

    def __init__(
        self,
        get_available_units: Callable[[], dict[int, Unit]],
        get_cost_data: Callable[[], tuple[float|None, float|None, int]],
        view: CostEditorView|None=None,
        parent: QWidget|None=None,
    ):
        """Initialise the controller."""
        super().__init__()

        # Build the view if it is not provided
        if view is None:
            view = CostEditorView(parent=parent)
        self.view = view

        # Stash the constructor arguments
        self._get_available_units = get_available_units
        self._get_cost_data = get_cost_data

        # Populate the units dropdown
        self.refresh_available_units()

        # Connect the view signals to the callback
        self.view.costChanged.connect(self.costUpdated.emit)

    def refresh(self):
        """Refresh the view with the latest cost data."""
        # Refresh the cost data fields
        cost_value, cost_qty_value, cost_qty_unit_id = self._get_cost_data()
        self.view.cost_value = cost_value
        self.view.cost_quantity_value = cost_qty_value
        self.view.cost_quantity_unit = cost_qty_unit_id
        # Refresh the available units
        self.refresh_available_units()

    def refresh_available_units(self):
        """Set the available units in the dropdown."""
        self.view.cost_qty_unit_dropdown.clear()
        for unit in self._get_available_units().values():
            self.view.cost_qty_unit_dropdown.add_unit(
                unit_display_name=unit.plural_display_name,
                unit_global_id=unit.id
            )