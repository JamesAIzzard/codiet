from typing import Callable

from codiet.models.units import Unit, IngredientUnitConversion
from codiet.views.units import StandardUnitEditorView, UnitConversionsEditorView
from codiet.views.dialog_box_views import EntityNameDialogView, OkDialogBoxView
from codiet.controllers.entity_name_dialog_ctrl import EntityNameDialogCtrl


class StandardUnitEditorCtrl:
    """A controller for the standard unit editor view."""

    def __init__(self,
            view: StandardUnitEditorView,
            unit_list: dict[int, Unit],
            on_standard_unit_changed: Callable[[int|None], None]
        ):
        """Initialise the standard unit editor controller."""
        self.view = view
        self._on_standard_unit_changed = on_standard_unit_changed
        # Initialise the units in the view
        # Add an empty item first
        self.view.cmb_standard_unit.add_unit(unit_display_name="", unit_global_id=None)
        for unit_id, unit in unit_list.items():
            self.view.cmb_standard_unit.add_unit(
                unit_display_name=unit.plural_display_name,
                unit_global_id=unit_id
            )

    def on_standard_unit_changed(self, unit_id: int):
        """Called when the standard unit is changed."""
        self._on_standard_unit_changed(unit_id)

class UnitConversionCtrl:
    def __init__(
        self,
        view: UnitConversionsEditorView,
        on_unit_conversion_added: Callable[[int, int, float, float], None],
    ):
        self.view = view