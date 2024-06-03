from typing import Callable

from codiet.models.measurements import CustomMeasurement
from codiet.views.measurements import MeasurementsDefinitionView

class MeasurementsDefinitionCtrl():
    def __init__(
            self, 
            view: MeasurementsDefinitionView,
            get_current_measurements: Callable[[], list[CustomMeasurement]],
            add_measurement: Callable[[CustomMeasurement], None],
        ):
        self.view = view
