from datetime import time

from codiet.tests.fixtures import BaseTestFixtures
from codiet.model.time import TimeWindow

class TimeTestFixtures(BaseTestFixtures):

    def create_time_window(self, start_time: str, end_time: str) -> TimeWindow:
        return TimeWindow(start_time=time.fromisoformat(start_time), end_time=time.fromisoformat(end_time))