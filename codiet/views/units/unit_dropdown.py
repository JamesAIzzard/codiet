from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QComboBox

from codiet.views import block_signals

class UnitDropdown(QComboBox):
    """A widget for selecting units.

    This class provides a dropdown widget for selecting units. It inherits from QComboBox,
    a Qt class for creating combo boxes.

    Signals:
        unitChanged: This signal is emitted when the selected unit changes. It carries the
            global ID of the unit as the argument.
    """

    unitChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        """Initialise the standard unit editor view.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        # When the combo box changes, emit the signal containing the
        # global id of the unit, which was stored in the userdata
        self.currentTextChanged.connect(
            lambda: self.unitChanged.emit(self.currentData())
        )

    @property
    def selected_unit_id(self) -> int:
        """Return the selected unit ID.

        Returns:
            int: The global ID of the unit.
        """
        return self.currentData()

    @selected_unit_id.setter
    def selected_unit_id(self, unit_id: int) -> None:
        """Set the selected unit ID.

        Args:
            unit_id (int): The global ID of the unit.
        """
        with block_signals(self):
            idx = self.findData(unit_id)
            self.setCurrentIndex(idx)

    @property
    def selected_unit_name(self) -> str:
        """Return the selected unit name.

        Returns:
            str: The display name of the unit.
        """
        return self.currentText()
    
    @selected_unit_name.setter
    def selected_unit_name(self, unit_name: str) -> None:
        """Set the selected unit by its display name.

        Args:
            unit_name (str): The display name of the unit.
        """
        with block_signals(self):
            idx = self.findText(unit_name)
            self.setCurrentIndex(idx)

    def add_unit(self, unit_display_name: str, unit_global_id: int) -> None:
        """Add a unit to the combo box.

        Args:
            unit_display_name (str): The display name of the unit.
            unit_global_id (int): The global ID of the unit.
        """
        self.addItem(unit_display_name, unit_global_id)

    def add_units(self, units: dict[int, str]) -> None:
        """Add a dictionary of units to the combo box.

        Args:
            units (dict[int|None, str]): A dictionary of units where the key is the
                global ID of the unit and the value is the display name.
        """
        for unit_global_id, unit_display_name in units.items():
            self.add_unit(unit_display_name, unit_global_id)

    def remove_unit(self, unit_global_id: int) -> None:
        """Remove a unit from the combo box.

        Args:
            unit_global_id (int): The global ID of the unit.
        """
        # Find the unit index based on the unit_global_id
        unit_index = self.findData(unit_global_id)
        if unit_index != -1:
            # Remove the unit
            self.removeItem(unit_index)

    def update_unit(self, unit_display_name: str, unit_global_id: int) -> None:
        """Update the display name of a unit.

        Args:
            unit_display_name (str): The new display name.
            unit_global_id (int): The global ID of the unit.
        """
        # Find the unit index based on the unit_global_id
        unit_index = self.findData(unit_global_id)
        if unit_index != -1:
            # Update the unit display name
            self.setItemText(unit_index, unit_display_name)
