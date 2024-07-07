from typing import Callable

from codiet.models.units import Unit
from codiet.views.cost import CostEditorView


class CostEditorCtrl:
    """Controller for the cost editor widget."""

    def __init__(
        self,
        view: CostEditorView,
        get_available_units: Callable[[], dict[int, Unit]],
        on_cost_changed: Callable[[float | None, float | None, int], None],
    ):
        """Initialise the controller."""
        self.view = view
        self._on_cost_changed_callback = on_cost_changed
        self._get_available_units = get_available_units
        # Populate the units dropdown
        self.set_available_units()

        # Connect the view signals to the callback
        self.view.costChanged.connect(self._on_cost_changed_callback)

    def set_cost_info(self, cost_value: float | None, cost_qty_value: float | None, cost_qty_unit_id: int):
        """Set the cost information."""
        self.view.cost_value = cost_value
        self.view.cost_quantity_value = cost_qty_value
        self.view.cost_quantity_unit = cost_qty_unit_id

    def set_available_units(self):
        """Set the available units in the dropdown."""
        self.view.cmb_cost_qty_unit.clear_units()
        for unit in self._get_available_units().values():
            self.view.cmb_cost_qty_unit.add_unit(
                unit_display_name=unit.plural_display_name,
                unit_global_id=unit.id
            )