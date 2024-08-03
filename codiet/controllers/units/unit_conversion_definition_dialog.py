from typing import Callable

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget

from codiet.utils.map import Map
from codiet.models.units.unit import Unit
from codiet.views.units.unit_conversion_definition_dialog_view import UnitConversionDefinitionDialogView
from codiet.controllers.search.search_column import SearchColumn

class UnitConversionDefinitionDialog(QObject):
    """A dialog box for defining a unit conversion."""
    
    conversionCreated = pyqtSignal(int, int)

    def __init__(
            self,
            get_global_units: Callable[[], dict[int, Unit]],
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

        # Stash constructor args
        self._check_conversion_available = check_conversion_available
        self._get_global_units = get_global_units

        # Init a map to convert unit names and IDs
        self._unit_name_id_map: Map[int, str] = Map(one_to_one=True)
        for unit in self._get_global_units().values():
            self._unit_name_id_map.add_mapping(unit.id, unit._unit_name)

        # Init the controllers for the to and from unit selectors
        self._from_unit_selector = SearchColumn(
            view=self.view.from_unit_selector,
            get_searchable_strings=lambda: [unit._unit_name for unit in self._get_global_units().values()],
            get_item_and_view_for_string=lambda unit_name: (unit_name, self._unit_name_id_map.get_keys(unit_name)[0]), # type: ignore
        )
        self._to_unit_selector = SearchColumn(
            view=self.view.to_unit_selector,
            get_searchable_strings=lambda: [unit._unit_name for unit in self._get_global_units().values()],
            get_item_and_view_for_string=lambda unit_name: (unit_name, self._unit_name_id_map.get_keys(unit_name)[0]), # type: ignore
        )

        # Connect to the view
        self.view.selectionChanged.connect(self._on_selection_changed)
        self.view.OKClicked.connect(self._on_OK_clicked)
        self.view.cancelClicked.connect(self.view.close)

    def _on_selection_changed(self, from_unit_id: int, to_unit_id: int) -> None:
        """Called when the selection is changed."""
        # Check if the conversion is available
        if self._check_conversion_available(from_unit_id, to_unit_id):
            self.view.btn_ok.setEnabled(True)
        else:
            self.view.btn_ok.setEnabled(False)

    def _on_OK_clicked(self, from_unit_id: int, to_unit_id: int) -> None:
        """Called when the OK button is clicked."""
        # Emit the conversionCreated signal with the from and to unit IDs
        self.conversionCreated.emit(from_unit_id, to_unit_id)

