from typing import Callable

from codiet.models.units import CustomUnit
from codiet.views.units import CustomUnitsDefinitionView

class CustomUnitsDefinitionCtrl():
    def __init__(
            self, 
            view: CustomUnitsDefinitionView,
            get_current_measurements: Callable[[], dict[str, CustomUnit]],
            add_measurement: Callable[[CustomUnit], None],
            remove_measurement: Callable[[str], None],
            update_measurement: Callable[[str, CustomUnit], None],
        ):
        self.view = view
