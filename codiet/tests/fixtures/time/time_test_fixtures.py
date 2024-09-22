from datetime import time

from codiet.tests.fixtures import BaseTestFixture
from codiet.model.time import TimeWindow

class TimeTestFixtures(BaseTestFixture):

    def create_time_window(self, start_time: str, end_time: str) -> TimeWindow:
        window = (time.fromisoformat(start_time), time.fromisoformat(end_time))
        return TimeWindow(window)