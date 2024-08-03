from unittest import TestCase
from datetime import time

from codiet.models.entity_serve_time_window import EntityServeTimeWindow

class TestEntityServeTimeWindow(TestCase):
    
        def setUp(self):
            pass
    
        def test_minimal_init(self):
            """Check we can initialise the window with only a parent ID."""
            window = EntityServeTimeWindow(parent_id=1)
            # Check its the right type
            self.assertIsInstance(window, EntityServeTimeWindow)
            # Check the window is default
            self.assertEqual(window.window, (time(0, 0), time(23, 59)))
            # Check the parent ID is correct
            self.assertEqual(window.primary_entity_id, 1)

        def test_init_with_window(self):
            """Check we can initialise the window with a window."""
            window = EntityServeTimeWindow(parent_id=1, window=(time(1, 0), time(2, 0)))
            # Check its the right type
            self.assertIsInstance(window, EntityServeTimeWindow)
            # Check the window is correct
            self.assertEqual(window.window, (time(1, 0), time(2, 0)))
            # Check the parent ID is correct
            self.assertEqual(window.primary_entity_id, 1)

        def test_time_in_window(self):
            """Check we can check if a time is in the window."""
            window = EntityServeTimeWindow(parent_id=1, window=(time(1, 0), time(2, 0)))
            # Check the time is in the window
            self.assertTrue(window.time_in_window(time(1, 30)))
            # Check the time is not in the window
            self.assertFalse(window.time_in_window(time(0, 30)))

        def test_is_subset_of(self):
            """Check we can check if a window is a subset of another window."""
            window = EntityServeTimeWindow(parent_id=1, window=(time(1, 0), time(2, 0)))
            other = EntityServeTimeWindow(parent_id=1, window=(time(0, 0), time(3, 0)))
            # Check the window is a subset
            self.assertTrue(window.is_subset_of(other))
            # Check the window is not a subset
            self.assertFalse(other.is_subset_of(window))

        def test_is_superset_of(self):
            """Check we can check if a window is a superset of another window."""
            window = EntityServeTimeWindow(parent_id=1, window=(time(1, 0), time(2, 0)))
            other = EntityServeTimeWindow(parent_id=1, window=(time(0, 0), time(3, 0)))
            # Check the window is a superset
            self.assertTrue(other.is_superset_of(window))
            # Check the window is not a superset
            self.assertFalse(window.is_superset_of(other))