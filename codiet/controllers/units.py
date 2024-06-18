from typing import Callable

from codiet.models.units import Unit
from codiet.views.units import CustomUnitsDefinitionView, CustomUnitView
from codiet.views.dialog_box_views import EntityNameDialogView, OkDialogBoxView
from codiet.controllers.entity_name_dialog_ctrl import EntityNameDialogCtrl


class CustomUnitsDefinitionCtrl:
    def __init__(
        self,
        view: CustomUnitsDefinitionView,
        get_custom_measurements: Callable[[], dict[int, Unit]],
        on_custom_unit_added: Callable[[str], Unit],
        on_custom_unit_edited: Callable[[Unit], None],
        on_custom_unit_removed: Callable[[int], None],
    ):
        self.view = view
        self.get_current_measurements = get_custom_measurements
        self.on_custom_unit_added = on_custom_unit_added
        self.on_custom_unit_edited = on_custom_unit_edited
        self.on_custom_unit_removed = on_custom_unit_removed
        # Create the dialog to collect and edit unit names
        self.unit_name_dialog = EntityNameDialogView(
            entity_name="Custom Unit", parent=self.view
        )
        self.unit_name_dialog.title = "Custom Unit Name"
        # Create the controller for the entity name dialog
        self.unit_name_dialog_ctrl = EntityNameDialogCtrl(
            self.unit_name_dialog,
            check_name_available=lambda name: name
            not in self.get_current_measurements(),
            on_name_accepted=self._on_accept_new_unit_name_clicked,
        )
        # Connect the signals
        self.view.addUnitClicked.connect(self._on_add_unit_clicked)
        self.view.removeUnitClicked.connect(self._on_remove_unit_clicked)
        self.view.editUnitClicked.connect(self._on_rename_unit_clicked)

    def load_custom_units_into_view(self, custom_units: dict[int, Unit]):
        """Load the custom units into the view."""
        for unit in custom_units.values():
            # Create a new view
            new_unit_view = self._create_new_unit_view(unit)
            # Add the new view
            self.view.lst_measurements.add_item(new_unit_view)

    def _create_new_unit_view(self, custom_unit: Unit):
        """Create a new unit view."""
        # Init a new view
        new_unit_view = CustomUnitView(unit_id=custom_unit.unit_id, unit_name=custom_unit.unit_name)
        # Set the custom unit values
        new_unit_view.custom_unit_qty = custom_unit.custom_unit_qty
        new_unit_view.std_unit_qty = custom_unit.std_unit_qty
        new_unit_view.std_unit_name = custom_unit.std_unit_name
        # Connect the new view signals to its handlers
        new_unit_view.customUnitQtyChanged.connect(self._on_custom_unit_qty_changed)
        new_unit_view.stdUnitQtyChanged.connect(self._on_std_unit_qty_changed)
        new_unit_view.stdUnitChanged.connect(self._on_std_unit_changed)
        return new_unit_view

    def _on_add_unit_clicked(self):
        """Called when the add measurement button is clicked."""
        # Set the name dialog handler to add a new unit
        self.unit_name_dialog_ctrl.set_accept_handler(
            self._on_accept_new_unit_name_clicked
        )
        # Clear the name dialog
        self.unit_name_dialog.clear()
        # Show the dialog
        self.unit_name_dialog.show()

    def _on_remove_unit_clicked(self, unit_id: int | None):
        """Called when the remove measurement button is clicked."""
        # If an item is not selected, open a popup to tell the user
        # they need to select a popup
        if unit_id is None:
            popup = OkDialogBoxView(
                title="No Measurement Selected",
                message="Please select a measurement to remove.",
                parent=self.view,
            )
            # Bind the OK signal to close the popup
            popup.okClicked.connect(popup.close)
            popup.show()
        else:
            # Remove the measurement from the view
            self.view.lst_measurements.remove_selected_item()
            # Call the callback
            self.on_custom_unit_removed(unit_id)

    def _on_rename_unit_clicked(self):
        """Called when the rename measurement button is clicked."""
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
            self.unit_name_dialog_ctrl.set_accept_handler(
                self._on_accept_edited_name_clicked
            )
            # Grab the existing measurement name
            existing_name = self.view.selected_unit_name
            assert existing_name is not None
            # Clear the name dialog
            self.unit_name_dialog.clear()
            # Set the existing name
            self.unit_name_dialog.entity_name = existing_name
            # Show the dialog
            self.unit_name_dialog.show()

    def _on_accept_new_unit_name_clicked(self, unit_name: str):
        """Called when the name dialog is accepted."""
        # Call the callback to get an id
        new_unit = self.on_custom_unit_added(unit_name)
        # Create a new view
        new_unit_view = self._create_new_unit_view(new_unit)
        # Add the new view
        self.view.lst_measurements.add_item(new_unit_view)
        # Close the dialog
        self.unit_name_dialog.close()

    def _on_accept_edited_name_clicked(self, new_name: str):
        """Called when the name dialog is accepted."""
        # Grab the id of the selected unit
        unit_id = self.view.selected_unit_id
        assert unit_id is not None
        # Update the unit name on the view
        self.view.change_unit_name(unit_id, new_name)
        # Grab the custom unit from the model
        custom_unit = self.get_current_measurements()[unit_id]
        # Call the callback
        self.on_custom_unit_edited(custom_unit)
        # Close the dialog
        self.unit_name_dialog.close()

    def _on_custom_unit_qty_changed(self, unit_id: int, value: float | None):
        """Called when the custom unit quantity changes."""
        # Grab the custom unit from the model
        custom_unit = self.get_current_measurements()[unit_id]
        # Update the custom unit value
        custom_unit.custom_unit_qty = value
        # Call the callback
        self.on_custom_unit_edited(custom_unit)

    def _on_std_unit_qty_changed(self, unit_id: int, value: float | None):
        """Called when the standard unit quantity changes."""
        # Grab the custom unit from the model
        custom_unit = self.get_current_measurements()[unit_id]
        # Update the standard unit value
        custom_unit.std_unit_qty = value
        # Call the callback
        self.on_custom_unit_edited(custom_unit)

    def _on_std_unit_changed(self, unit_id: int, value: str):
        """Called when the standard unit changes."""
        # Grab the custom unit from the model
        custom_unit = self.get_current_measurements()[unit_id]
        # Update the standard unit name
        custom_unit.std_unit_name = value
        # Call the callback
        self.on_custom_unit_edited(custom_unit)
