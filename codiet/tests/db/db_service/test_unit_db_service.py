from codiet.tests.db import DatabaseTestCase
from codiet.db_population.units import read_units_from_json
from codiet.db.database_service.unit_db_service import UnitDBService

class TestUnitDBService(DatabaseTestCase):

    def setUp(self):
        super().setUp()

        # Read the global units from the JSON file
        self.units = read_units_from_json()

        # Save the units to the database
        self.db_service.units.create_units(self.units)

    def test_create_and_read_units(self):
        # Read the units from the database
        units = self.db_service.units.read_all_units()

        # Check that the units are the same
        self.assertEqual(units, self.units)

        # Check that all units are persisted
        for unit in units:
            self.assertTrue(unit.is_persisted)

