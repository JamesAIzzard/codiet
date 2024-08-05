from codiet.tests.db import DatabaseTestCase

class TestUnitRepository(DatabaseTestCase):

    def setUp(self) -> None:
        super().setUp()

        self.unit_1_data = {
            "unit_name": "unit_1",
            "single_display_name": "unit_1",
            "plural_display_name": "unit_1s",
            "unit_type": "unit",
        }
        self.unit_2_data = {
            "unit_name": "unit_2",
            "single_display_name": "unit_2",
            "plural_display_name": "unit_2s",
            "unit_type": "unit",
        }

    def _create_test_units(self):
        """Create some test units."""
        # Create the bases
        self.unit_1_id = self.repository.units.create_unit_base(
            unit_name=self.unit_1_data["unit_name"],
            single_display_name=self.unit_1_data["single_display_name"],
            plural_display_name=self.unit_1_data["plural_display_name"],
            unit_type=self.unit_1_data["unit_type"],
        )

        self.unit_2_id = self.repository.units.create_unit_base(
            unit_name=self.unit_2_data["unit_name"],
            single_display_name=self.unit_2_data["single_display_name"],
            plural_display_name=self.unit_2_data["plural_display_name"],
            unit_type=self.unit_2_data["unit_type"],
        )

        # Create the aliases
        self.repository.units.create_unit_alias(
            alias="unit_1_alias_1", primary_unit_id=self.unit_1_id
        )
        self.repository.units.create_unit_alias(
            alias="unit_1_alias_2", primary_unit_id=self.unit_1_id
        )
        self.repository.units.create_unit_alias(
            alias="unit_2_alias", primary_unit_id=self.unit_2_id
        )
        self.repository.units.create_unit_alias(
            alias="unit_2_alias_2", primary_unit_id=self.unit_2_id
        )

    def test_create_and_read_unit_base(self):
        """Test creating a global unit."""
        # Create the unit
        unit_1_id = self.repository.units.create_unit_base(
            unit_name=self.unit_1_data["unit_name"],
            single_display_name=self.unit_1_data["single_display_name"],
            plural_display_name=self.unit_1_data["plural_display_name"],
            unit_type=self.unit_1_data["unit_type"],
        )

        # Check the ID is correct
        self.assertEqual(unit_1_id, 1)

        # Check the unit is in the database
        unit_1 = self.repository.units.read_unit_base(unit_1_id)
        self.assertEqual(unit_1["unit_name"], self.unit_1_data["unit_name"])
        self.assertEqual(unit_1["single_display_name"], self.unit_1_data["single_display_name"])
        self.assertEqual(unit_1["plural_display_name"], self.unit_1_data["plural_display_name"])
        self.assertEqual(unit_1["unit_type"], self.unit_1_data["unit_type"])

    def test_read_all_unit_bases(self):
        """Test reading all global units."""
        # Create the units
        self._create_test_units()

        # Check the units are in the database
        units = self.repository.units.read_all_unit_bases()
        self.assertEqual(len(units), 2)

        # Check the first unit
        self.assertEqual(units[0]["unit_name"], self.unit_1_data["unit_name"])
        self.assertEqual(units[0]["single_display_name"], self.unit_1_data["single_display_name"])
        self.assertEqual(units[0]["plural_display_name"], self.unit_1_data["plural_display_name"])
        self.assertEqual(units[0]["unit_type"], self.unit_1_data["unit_type"])

        # Check the second unit
        self.assertEqual(units[1]["unit_name"], self.unit_2_data["unit_name"])
        self.assertEqual(units[1]["single_display_name"], self.unit_2_data["single_display_name"])
        self.assertEqual(units[1]["plural_display_name"], self.unit_2_data["plural_display_name"])
        self.assertEqual(units[1]["unit_type"], self.unit_2_data["unit_type"])

    def test_create_and_read_unit_aliases(self):
        """Test creating and reading unit aliases."""
        # Create the units
        self._create_test_units()

        # Check the aliases are in the database
        unit_1_aliases = self.repository.units.read_unit_aliases(self.unit_1_id)
        self.assertEqual(len(unit_1_aliases), 2)
        self.assertEqual(unit_1_aliases[0], "unit_1_alias_1")
        self.assertEqual(unit_1_aliases[1], "unit_1_alias_2")

        unit_2_aliases = self.repository.units.read_unit_aliases(self.unit_2_id)
        self.assertEqual(len(unit_2_aliases), 2)
        self.assertEqual(unit_2_aliases[0], "unit_2_alias")
        self.assertEqual(unit_2_aliases[1], "unit_2_alias_2")

    def test_update_unit_base(self):
        """Test updating a global unit."""
        # Create the test units
        self._create_test_units()

        # Check the values of the first
        unit_1 = self.repository.units.read_unit_base(self.unit_1_id)
        self.assertEqual(unit_1["unit_name"], self.unit_1_data["unit_name"])
        self.assertEqual(unit_1["single_display_name"], self.unit_1_data["single_display_name"])
        self.assertEqual(unit_1["plural_display_name"], self.unit_1_data["plural_display_name"])
        self.assertEqual(unit_1["unit_type"], self.unit_1_data["unit_type"])

        # Update the first unit
        self.repository.units.update_unit_base(
            unit_id=self.unit_1_id,
            unit_name="new_unit_name",
            single_display_name="new_single_display_name",
            plural_display_name="new_plural_display_name",
            unit_type="new_unit_type",
        )

        # Check the values of the first unit again
        unit_1 = self.repository.units.read_unit_base(self.unit_1_id)
        self.assertEqual(unit_1["unit_name"], "new_unit_name")
        self.assertEqual(unit_1["single_display_name"], "new_single_display_name")
        self.assertEqual(unit_1["plural_display_name"], "new_plural_display_name")
        self.assertEqual(unit_1["unit_type"], "new_unit_type")

    def test_delete_unit_base(self):
        """Test deleting a global unit."""
        # Create the test units
        self._create_test_units()

        # Check the units are in the database
        units = self.repository.units.read_all_unit_bases()
        self.assertEqual(len(units), 2)

        # Delete the first unit
        self.repository.units.delete_unit_base(self.unit_1_id)

        # Check that only the second unit is in the database
        units = self.repository.units.read_all_unit_bases()
        self.assertEqual(len(units), 1)
        
