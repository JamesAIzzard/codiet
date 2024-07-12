from typing import Callable

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget

from codiet.models.units import Unit
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
        
        # Connect signals and slots
        self.view.onUnitChanged.connect(self.onUnitChanged.emit)

        # Stash the source of available units
        self._get_available_units = get_available_units

        # Populate units on the view
        self.reset_available_units()

    @property
    def selected_unit_id(self) -> int:
        """Return the global ID of the selected unit."""
        return self.view.unit_dropdown.selected_unit_id
    
    @selected_unit_id.setter
    def selected_unit_id(self, unit_id: int):
        """Set the selected unit by its global ID."""
        self.view.unit_dropdown.selected_unit_id = unit_id

    def reset_available_units(self) -> None:
        """Reset the available units in the view."""
        # Grab the available units
        units = self._get_available_units()
        # Clear the old ones
        self.view.unit_dropdown.clear()
        # For each unit from the source
        for unit_id, unit in units.items():
            # Add it to the view
            self.view.unit_dropdown.addItem(unit.plural_display_name, unit_id)