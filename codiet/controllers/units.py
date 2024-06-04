from typing import Callable

from codiet.models.units import CustomUnit
from codiet.views.units import CustomUnitsDefinitionView, CustomUnitView
from codiet.views.dialog_box_views import EntityNameDialogView
from codiet.controllers.entity_name_dialog_ctrl import EntityNameDialogCtrl


class CustomUnitsDefinitionCtrl:
    def __init__(
        self,
        view: CustomUnitsDefinitionView,
        get_current_measurements: Callable[[], dict[str, CustomUnit]],
        add_measurement: Callable[[CustomUnit], None],
        remove_measurement: Callable[[str], None],
        update_measurement: Callable[[str, CustomUnit], None],
    ):
        self.view = view
        self.get_current_measurements = get_current_measurements
        self.add_measurement = add_measurement
        self.remove_measurement = remove_measurement
        self.update_measurement = update_measurement
        # Create the dialog to collect and edit unit names
        self.unit_name_dialog = EntityNameDialogView(
            entity_name="Custom Unit", parent=self.view
        )
        self.unit_name_dialog.title = "Custom Unit Name"
        # Create the controller for the entity name dialog
        self.unit_name_dialog_ctrl = EntityNameDialogCtrl(
            self.unit_name_dialog,
            check_name_available=lambda name: name not in self.get_current_measurements(),
            on_name_accepted=self._on_accept_name_clicked,
        )
        # Connect the signals
        self.view.addMeasurementClicked.connect(self._on_add_measurement_clicked)

    def _on_add_measurement_clicked(self):
        """Called when the add measurement button is clicked."""
        # Clear the name dialog
        self.unit_name_dialog.clear()
        # Show the dialog
        self.unit_name_dialog.show()

    def _on_accept_name_clicked(self, name: str):
        """Called when the name dialog is accepted."""
        # Create a new custom unit
        new_unit = CustomUnit(unit_name=name, unit_to_grams_ratio=1)
        # Add the new unit to the view
        # Init a new view
        new_unit_view = CustomUnitView(qty_name=name)
        # Add the new view
        self.view.lst_measurements.add_item(new_unit_view)
        # Call the callback
        self.add_measurement(new_unit)
        # Close the dialog
        self.unit_name_dialog.close()
