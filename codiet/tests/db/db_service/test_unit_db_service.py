from codiet.tests.db import DatabaseTestCase
from codiet.db_population.units import read_units_from_json, read_global_unit_conversions_from_json
from codiet.models.units.unit import Unit

class TestUnitDBService(DatabaseTestCase):

    def setUp(self):
        super().setUp()

    def test_unit_id_name_map(self):
        """Checks that the unit ID to name map is correct."""
        # Put the set of units into the database
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Check the length of the map is the same as the number of units
        self.assertEqual(len(self.db_service.units.unit_id_name_map), len(units_from_json))

        # Check that the map is correct
        for unit in units_from_json:
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

    def test_units(self):
        """Checks that the units are correct."""
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Check the length of the units is the same as the number of units
        self.assertEqual(len(units_from_json), len(self.db_service.units.units))

        # Check each unit is in the units
        for unit in units_from_json:
            self.assertIn(unit, self.db_service.units.units)

    def test_gram_unit(self):
        """Checks that the gram unit is correct."""
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Check the gram unit is accessible
        gram_unit = self.db_service.units.gram
        self.assertEqual(gram_unit.unit_name, "gram")

    def test_mass_units(self):
        """Checks that the mass units are correct."""
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Count the number of units with mass type from the json
        mass_units_from_json = [unit for unit in units_from_json if unit.type == "mass"]
        self.assertEqual(len(mass_units_from_json), len(self.db_service.units.mass_units))

        # Check each unit is in the mass units
        for unit in mass_units_from_json:
            self.assertIn(unit, self.db_service.units.mass_units)

    def test_volume_units(self):
        """Checks that the volume units are correct."""
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Count the number of units with volume type from the json
        volume_units_from_json = [unit for unit in units_from_json if unit.type == "volume"]
        self.assertEqual(len(volume_units_from_json), len(self.db_service.units.volume_units))

        # Check each unit is in the volume units
        for unit in volume_units_from_json:
            self.assertIn(unit, self.db_service.units.volume_units)

    def test_group_units(self):
        """Checks that the group units are correct."""
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Count the number of units with group type from the json
        group_units_from_json = [unit for unit in units_from_json if unit.type == "grouping"]
        self.assertEqual(len(group_units_from_json), len(self.db_service.units.grouping_units))

        # Check each unit is in the group units
        for unit in group_units_from_json:
            self.assertIn(unit, self.db_service.units.grouping_units)

    def test_get_unit_by_name(self):
        """Checks that we can get a unit by its name."""
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Check we can get the kg unit
        kg_unit = self.db_service.units.get_unit_by_name("kilogram")

        # Check the name is correct
        self.assertEqual(kg_unit.unit_name, "kilogram")

    def test_get_unit_by_id(self):
        """Checks that we can get a unit by its ID."""
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Check we can get the kg unit
        kg_unit = self.db_service.units.get_unit_by_name("kilogram")

        # Check we can get the unit by its ID
        kg_unit_by_id = self.db_service.units.get_unit_by_id(kg_unit.id) # type: ignore

        # Check the name is correct
        self.assertEqual(kg_unit_by_id.unit_name, "kilogram")

    def test_create_and_read_units(self):
        """Check we can read and write units to the database."""
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Read the units from the database
        units = self.db_service.units.read_all_units()

        # Check that the units are the same
        self.assertEqual(units, units_from_json)

        # Check that all units are persisted
        for unit in units:
            self.assertTrue(unit.is_persisted)

    def test_create_and_read_global_unit_conversions(self):
        """Check we can read and write unit conversions to the database."""
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)
        unit_conversions_from_json = read_global_unit_conversions_from_json()
        self.db_service.units.create_global_unit_conversions(unit_conversions_from_json)

        # Read the unit conversions from the database
        unit_conversions = self.db_service.units.read_all_global_unit_conversions()

        # Check that the unit conversions are the same
        self.assertEqual(unit_conversions, unit_conversions_from_json)

        # Check that all unit conversions are persisted
        for unit_conversion in unit_conversions:
            self.assertTrue(unit_conversion.is_persisted)

    def test_update_units(self):
        """Checks that we can update a unit in the database.
        Also confirms the caching updates correctly.
        """
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

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
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Grab the kilogram unit
        kg_unit = self.db_service.units.get_unit_by_name("kilogram")

        # Delete the unit
        self.db_service.units.delete_units(set([kg_unit]))

        # Assert we get a key error when trying to get the unit
        with self.assertRaises(KeyError):
            self.db_service.units.get_unit_by_name("kilogram")

        self.assertNotIn(kg_unit, self.db_service.units.units)

