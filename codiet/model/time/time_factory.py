from typing import TYPE_CHECKING
from datetime import time

from codiet.model.time.time_window import TimeWindow

if TYPE_CHECKING:
    from codiet.model.time import TimeWindowDTO

class TimeFactory:
    
    def create_time_window_from_dto(self, time_window_dto:"TimeWindowDTO") -> TimeWindow:
        start = time.fromisoformat(time_window_dto['start_hh_mm'])
        end = time.fromisoformat(time_window_dto['end_hh_mm'])
        return TimeWindow(
            start_time=start,
            end_time=end
        )