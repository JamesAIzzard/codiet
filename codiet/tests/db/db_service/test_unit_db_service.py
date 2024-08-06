from codiet.tests.db import DatabaseTestCase
from codiet.db_population.units import read_units_from_json
from codiet.models.units.unit import Unit

class TestUnitDBService(DatabaseTestCase):

    def setUp(self):
        super().setUp()

        # Read the global units from the JSON file
        self.units_from_json = read_units_from_json()

        # Save the units to the database
        self.db_service.units.create_units(self.units_from_json)

    def test_unit_id_name_map(self):
        """Checks that the unit ID to name map is correct."""
        # Check the length of the map is the same as the number of units
        self.assertEqual(len(self.db_service.units.unit_id_name_map), len(self.units_from_json))

        # Check that the map is correct
        for unit in self.units_from_json:
            # Check that the unit is in the map
            self.assertIn(unit.id, self.db_service.units.unit_id_name_map.keys)

        # Create a new unit and add it to the database
        new_unit = Unit(
            unit_name="newunit",
            single_display_name="New Unit",
            plural_display_name="New Units",
            type="newtype",
            aliases=set(["newalias"])
        )
        self.db_service.units.create_units(set([new_unit]))

        # Check that the map is updated
        self.assertIn(new_unit.id, self.db_service.units.unit_id_name_map.keys)

    def test_mass_units(self):
        """Checks that the mass units are correct."""
        # Count the number of units with mass type from the json
        mass_units_from_json = [unit for unit in self.units_from_json if unit.type == "mass"]
        self.assertEqual(len(mass_units_from_json), len(self.db_service.units.mass_units))

        # Check each unit is in the mass units
        for unit in mass_units_from_json:
            self.assertIn(unit, self.db_service.units.mass_units)

    def test_volume_units(self):
        """Checks that the volume units are correct."""
        # Count the number of units with volume type from the json
        volume_units_from_json = [unit for unit in self.units_from_json if unit.type == "volume"]
        self.assertEqual(len(volume_units_from_json), len(self.db_service.units.volume_units))

        # Check each unit is in the volume units
        for unit in volume_units_from_json:
            self.assertIn(unit, self.db_service.units.volume_units)

    def test_group_units(self):
        """Checks that the group units are correct."""
        # Count the number of units with group type from the json
        group_units_from_json = [unit for unit in self.units_from_json if unit.type == "grouping"]
        self.assertEqual(len(group_units_from_json), len(self.db_service.units.grouping_units))

        # Check each unit is in the group units
        for unit in group_units_from_json:
            self.assertIn(unit, self.db_service.units.grouping_units)

    def test_get_unit_by_name(self):
        """Checks that we can get a unit by its name."""
        # Check we can get the kg unit
        kg_unit = self.db_service.units.get_unit_by_name("kilogram")
        
        # Check the name is correct
        self.assertEqual(kg_unit.unit_name, "kilogram")

    def test_create_and_read_units(self):
        """Check we can read and write units to the database."""
        # Write happens in the setUp method
        # Read the units from the database
        units = self.db_service.units.read_all_units()

        # Check that the units are the same
        self.assertEqual(units, self.units_from_json)

        # Check that all units are persisted
        for unit in units:
            self.assertTrue(unit.is_persisted)

    def test_update_units(self):
        """Checks that we can update a unit in the database.
        Also confirms the caching updates correctly.
        """
        # Read the units from the database
        units = self.db_service.units.read_all_units()

        # Grab the kilogram unit and update
        kg_unit = self.db_service.units.get_unit_by_name("kilogram")
        # Modify it (modify private variables because we don't provide setters right now)
        kg_unit._single_display_name = "modifiedkg"
        kg_unit._plural_display_name = "modifiedkgs"
        kg_unit._type = "modifiedtype"
        kg_unit._aliases = set(["modifiedkgalias"])

        # Update the unit
        self.db_service.units.update_units(set([kg_unit]))

        # Read the units from the database
        updated_kg = self.db_service.units.get_unit_by_name("kilogram")

        # Check that the unit is updated
        self.assertEqual(updated_kg, kg_unit)
        self.assertEqual(updated_kg.single_display_name, "modifiedkg")
        self.assertEqual(updated_kg.plural_display_name, "modifiedkgs")
        self.assertEqual(updated_kg.type, "modifiedtype")
        self.assertEqual(updated_kg.aliases, set(["modifiedkgalias"]))

    def test_delete_units(self):
        """Checks that we can delete a unit from the database.
        Also confirms the caching updates correctly.
        """
        # Grab the kilogram unit
        kg_unit = self.db_service.units.get_unit_by_name("kilogram")

        # Delete the unit
        self.db_service.units.delete_units(set([kg_unit]))

        # Assert we get a key error when trying to get the unit
        with self.assertRaises(KeyError):
            self.db_service.units.get_unit_by_name("kilogram")

        self.assertNotIn(kg_unit, self.db_service.units.units)

