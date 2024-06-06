from typing import Callable

from codiet.models.units import CustomUnit
from codiet.views.units import CustomUnitsDefinitionView, CustomUnitView
from codiet.views.dialog_box_views import EntityNameDialogView, OkDialogBoxView
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
            on_name_accepted=self._on_accept_new_name_clicked,
        )
        # Connect the signals
        self.view.addMeasurementClicked.connect(self._on_add_measurement_clicked)
        self.view.removeMeasurementClicked.connect(self._on_remove_measurement_clicked)
        self.view.editMeasurementClicked.connect(self._on_edit_measurement_clicked)

    def _on_add_measurement_clicked(self):
        """Called when the add measurement button is clicked."""
        # Set the name dialog handler to add a new unit
        self.unit_name_dialog_ctrl.set_accept_handler(self._on_accept_new_name_clicked)
        # Clear the name dialog
        self.unit_name_dialog.clear()
        # Show the dialog
        self.unit_name_dialog.show()

    def _on_remove_measurement_clicked(self, measurement_name: str | None):
        """Called when the remove measurement button is clicked."""
        # If an item is not selected, open a popup to tell the user
        # they need to select a popup
        if measurement_name is None:
            popup = OkDialogBoxView(
                title="No Measurement Selected",
                message="Please select a measurement to remove.",
                parent=self.view,
            )
            # Bind the OK signal to close the popup
            popup.okClicked.connect(popup.close)
            popup.show()
        else:
            # Remove the unit from the view
            self.view.lst_measurements.remove_selected_item()
            # Call the callback
            self.remove_measurement(measurement_name)

    def _on_edit_measurement_clicked(self):
        """Called when the edit measurement button is clicked."""
        # If an item is not selected, open a popup to tell the user
        # they need to select a popup
        if not self.view.lst_measurements.item_is_selected:
            popup = OkDialogBoxView(
                title="No Measurement Selected",
                message="Please select a measurement to edit.",
                parent=self.view,
            )
            # Bind the OK signal to close the popup
            popup.okClicked.connect(popup.close)
            popup.show()
        else:
            # Set the name dialog handler to edit the selected unit
            self.unit_name_dialog_ctrl.set_accept_handler(self._on_accept_edited_name_clicked)
            # Grab the existing measurement name
            existing_name = self.view.selected_measurement_name
            assert existing_name is not None
            # Clear the name dialog
            self.unit_name_dialog.clear()
            # Set the existing name
            self.unit_name_dialog.entity_name = existing_name
            # Show the dialog
            self.unit_name_dialog.show()

    def _on_accept_new_name_clicked(self, name: str):
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

    def _on_accept_edited_name_clicked(self, new_name:str):
        """Called when the name dialog is accepted."""
        # Grab the currently selected widget
        selected_view = self.view.selected_measurement_view
        assert selected_view is not None
        # Grab its old name
        old_name = selected_view.quantity_name
        # Grab the custom unit from the model
        custom_unit = self.get_current_measurements()[old_name]
        # Update the name on the unit
        custom_unit.unit_name = new_name
        # Update the unit name on the view
        selected_view.quantity_name = new_name
        # Call the callback
        self.update_measurement(old_name, custom_unit)
        # Close the dialog
        self.unit_name_dialog.close()

