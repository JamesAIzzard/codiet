from typing import Callable

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget

from codiet.model.quantities.unit import Unit
from codiet.views.units.standard_unit_editor_view import StandardUnitEditorView

class StandardUnitEditor(QObject):
    """A controller for the standard unit editor view.
    This module can be used to control to control the standard unit for an entity.
    
    Signals:
        onUnitChanged: Emitted when the standard unit is changed.
            Has a single argument, the new standard unit id (int).
    """

    onUnitChanged = pyqtSignal(int)

    def __init__(
        self,
        get_available_units: Callable[[], dict[int, Unit]],
        view: StandardUnitEditorView|None = None,
        parent: QWidget|None = None,
    ):
        """Initialise the standard unit editor controller.
        Args:
            get_available_units (Callable[[], dict[int, Unit]]): A function that
                returns a dictionary of available units.
            view (StandardUnitEditorView): The view to control.
            parent (QWidget): The parent widget.
        """
        super().__init__()

        # Build the view if it is not provided
        if view is None:
            view = StandardUnitEditorView(parent=parent or None)
        self.view = view
        
        # Stash the constructor args
        self._get_available_units = get_available_units

        # Connect signals and slots
        self.view.onUnitChanged.connect(self.onUnitChanged.emit)

        # Populate the units
        self.set_available_units(get_available_units=get_available_units)

    @property
    def selected_unit(self) -> int:
        """Return the ID of the selected unit."""
        return self.view.unit_dropdown.selected_unit_id
    
    @selected_unit.setter
    def selected_unit(self, unit_id: int) -> None:
        """Set the selected unit."""
        self.view.unit_dropdown.selected_unit_id = unit_id

    def set_available_units(self, get_available_units: Callable[[],dict[int, Unit]]) -> None:
        """Set the function to get available units."""
        # Update the source callback on the module
        self._get_available_units = get_available_units
        # Update the available units on the view
        # Clear the old ones
        self.view.unit_dropdown.clear()
        # For each unit from the source
        for unit_id, unit in get_available_units().items():
            # Add it to the view
            self.view.unit_dropdown.addItem(unit._plural_display_name, unit_id)
