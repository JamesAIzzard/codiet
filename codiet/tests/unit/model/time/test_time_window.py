"""Tests for the TimeWindow model."""

from datetime import time

from codiet.tests import BaseModelTest
from codiet.model.time import TimeWindow

class BaseTimeWindowTest(BaseModelTest):
    """Base class for testing the TimeWindow class."""
    
    def setUp(self) -> None:
        super().setUp()

class TestConstructor(BaseTimeWindowTest):
    
        def test_minimal_init(self):
            """Check we can initialise the window with no arguments."""
            window = TimeWindow()
            self.assertIsInstance(window, TimeWindow)

        def test_default_window(self):
            """Check the default window is set correctly."""
            window = TimeWindow()
            self.assertEqual(window.window, (time(0, 0), time(23, 59)))

        def test_init_with_window(self):
            """Check we can initialise the window with a window."""
            times = (time(1, 0), time(2, 0))
            window = TimeWindow(window=times)
            self.assertEqual(window.window, times)

class TestTimeInWindow(BaseTimeWindowTest):

        def test_returns_true_if_time_in_window(self):
            """Check the method returns True if the time is in the window."""
            window = TimeWindow(window=(time(1, 0), time(2, 0)))
            self.assertTrue(window.time_in_window(time(1, 30)))

        def test_returns_false_if_time_not_in_window(self):
            """Check the method returns False if the time is not in the window."""
            window = TimeWindow(window=(time(1, 0), time(2, 0)))
            self.assertFalse(window.time_in_window(time(3, 0)))

class TestIsSubsetOf(BaseTimeWindowTest):

        def test_returns_true_if_window_is_subset(self):
            """Check the method returns True if the window is a subset of another window."""
            window = TimeWindow(window=(time(1, 0), time(2, 0)))
            other = TimeWindow(window=(time(0, 0), time(3, 0)))
            self.assertTrue(window.is_subset_of(other))

        def test_returns_false_if_window_is_not_subset(self):
            """Check the method returns False if the window is not a subset of another window."""
            window = TimeWindow(window=(time(1, 0), time(2, 0)))
            other = TimeWindow(window=(time(0, 0), time(1, 30)))
            self.assertFalse(window.is_subset_of(other))

class TestIsSupersetOf(BaseTimeWindowTest):
     
        def test_returns_true_if_window_is_superset(self):
            """Check the method returns True if the window is a superset of another window."""
            window = TimeWindow(window=(time(0, 0), time(3, 0)))
            other = TimeWindow(window=(time(1, 0), time(2, 0)))
            self.assertTrue(window.is_superset_of(other))

        def test_returns_false_if_window_is_not_superset(self):
            """Check the method returns False if the window is not a superset of another window."""
            window = TimeWindow(window=(time(0, 0), time(1, 30)))
            other = TimeWindow(window=(time(1, 0), time(2, 0)))
            self.assertFalse(window.is_superset_of(other))