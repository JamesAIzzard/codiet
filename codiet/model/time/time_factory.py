from typing import TYPE_CHECKING

from .time_window import TimeWindow
from .utils import parse_time_string

if TYPE_CHECKING:
    from codiet.model.time import TimeWindowDTO


class TimeFactory:

    def create_time_window_from_dto(
        self, time_window_dto: "TimeWindowDTO"
    ) -> TimeWindow:

        start = parse_time_string(time_window_dto["start_hh_mm"])
        end = parse_time_string(time_window_dto["end_hh_mm"])

        return TimeWindow(start_time=start, end_time=end)
