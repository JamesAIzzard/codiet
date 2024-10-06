from typing import TYPE_CHECKING, TypedDict

from datetime import time

class TimeWindowDTO(TypedDict):
    start_hh_mm: str
    end_hh_mm: str

class TimeWindow:
    def __init__(
            self,
            start_time: time,
            end_time: time,
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)

        self._start_time = start_time
        self._end_time = end_time

    @property
    def start_time(self) -> time:
        return self._start_time
    
    @start_time.setter
    def start_time(self, start_time: time) -> None:
        self._start_time = start_time

    @property
    def end_time(self) -> time:
        return self._end_time
    
    @end_time.setter
    def end_time(self, end_time: time) -> None:
        self._end_time = end_time

    @property
    def window(self) -> tuple[time, time]:
        return (self._start_time, self._end_time)
    
    @window.setter
    def window(self, window: tuple[time, time]) -> None:
        self._window = window

    def time_in_window(self, time: time) -> bool:
        return self._window[0] <= time <= self._window[1]
    
    def is_subset_of(self, other: 'TimeWindow') -> bool:
        return other._window[0] <= self._window[0] and other._window[1] >= self._window[1]
    
    def is_superset_of(self, other: 'TimeWindow') -> bool:
        return self._window[0] <= other._window[0] and self._window[1] >= other._window[1]