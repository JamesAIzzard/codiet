from typing import Callable

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget

from codiet.models.units.unit import Unit
from codiet.views.units.unit_conversion_definition_dialog_view import UnitConversionDefinitionDialogView

class UnitConversionDefinitionDialog(QObject):
    """A dialog box for defining a unit conversion."""
    
    conversionCreated = pyqtSignal(int, int)

    def __init__(
            self,
            global_units: dict[int, Unit],
            check_conversion_available: Callable[[int, int], bool],
            view: UnitConversionDefinitionDialogView | None = None,
            parent: QWidget | None = None,
    ):
        """Initialise the unit conversion definition dialog."""
        super().__init__()

        # Build the view if it is not provided
        if view is None:
            view = UnitConversionDefinitionDialogView(parent=parent)
        self.view = view

        # Stash list of global units
        self._global_units = global_units
        # Stash the method to check if a conversion is available
        self.check_conversion_available = check_conversion_available

        # Connect to the view
        self.view.selectionChanged.connect(self._on_selection_changed)
        self.view.OKClicked.connect(self._on_OK_clicked)
        self.view.cancelClicked.connect(self._on_cancel_clicked)

    def _on_selection_changed(self, from_unit_id: int, to_unit_id: int) -> None:
        """Called when the selection is changed."""
        # Check if the conversion is available
        if self.check_conversion_available(from_unit_id, to_unit_id):
            self.view.btn_ok.setEnabled(True)
        else:
            self.view.btn_ok.setEnabled(False)

    def _on_OK_clicked(self, from_unit_id: int, to_unit_id: int) -> None:
        """Called when the OK button is clicked."""
        # Emit the conversionCreated signal with the from and to unit IDs
        self.conversionCreated.emit(from_unit_id, to_unit_id)

    def _on_cancel_clicked(self) -> None:
        """Called when the cancel button is clicked."""
        # Close the dialog
        self.view.close()

