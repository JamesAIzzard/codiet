from codiet.tests.db.database_test_case import DatabaseTestCase

class TestUnitRepository(DatabaseTestCase):

    def setUp(self) -> None:
        super().setUp()

        # Create some unit test data
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

        # Create some global unit conversion data
        self.unit_conversion_1_data = {
            "from_unit_id": 1,
            "to_unit_id": 2,
            "from_unit_qty": 1,
            "to_unit_qty": 2,
        }
        self.unit_conversion_2_data = {
            "from_unit_id": 2,
            "to_unit_id": 1,
            "from_unit_qty": 2,
            "to_unit_qty": 1,
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

    def _create_test_unit_conversions(self):
        """Create some test unit conversions."""
        # Create the conversions
        self.repository.units.create_global_unit_conversion(
            from_unit_id=self.unit_conversion_1_data["from_unit_id"],
            to_unit_id=self.unit_conversion_1_data["to_unit_id"],
            from_unit_qty=self.unit_conversion_1_data["from_unit_qty"],
            to_unit_qty=self.unit_conversion_1_data["to_unit_qty"],
        )

        self.repository.units.create_global_unit_conversion(
            from_unit_id=self.unit_conversion_2_data["from_unit_id"],
            to_unit_id=self.unit_conversion_2_data["to_unit_id"],
            from_unit_qty=self.unit_conversion_2_data["from_unit_qty"],
            to_unit_qty=self.unit_conversion_2_data["to_unit_qty"],
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
        aliases = self.repository.units.read_unit_aliases(unit_id=self.unit_1_id)

        # Check we got the right number back
        self.assertEqual(len(aliases), 2)

        # Check the first alias
        self.assertEqual(aliases[1], "unit_1_alias_1")
        self.assertEqual(aliases[2], "unit_1_alias_2")

    def test_create_and_read_unit_conversions(self):
        """Test creating and reading global unit conversions."""
        # Create the units
        self._create_test_units()

        # Create the conversions
        self._create_test_unit_conversions()

        # Check the conversions are in the database
        conversions = self.repository.units.read_all_global_unit_conversions()

        # Check we got the right number back
        self.assertEqual(len(conversions), 2)

        # Check the first conversion
        self.assertEqual(conversions[0]["from_unit_id"], self.unit_conversion_1_data["from_unit_id"])
        self.assertEqual(conversions[0]["to_unit_id"], self.unit_conversion_1_data["to_unit_id"])
        self.assertEqual(conversions[0]["from_unit_qty"], self.unit_conversion_1_data["from_unit_qty"])
        self.assertEqual(conversions[0]["to_unit_qty"], self.unit_conversion_1_data["to_unit_qty"])

        # Check the second conversion
        self.assertEqual(conversions[1]["from_unit_id"], self.unit_conversion_2_data["from_unit_id"])
        self.assertEqual(conversions[1]["to_unit_id"], self.unit_conversion_2_data["to_unit_id"])
        self.assertEqual(conversions[1]["from_unit_qty"], self.unit_conversion_2_data["from_unit_qty"])
        self.assertEqual(conversions[1]["to_unit_qty"], self.unit_conversion_2_data["to_unit_qty"])

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

    def test_update_global_unit_conversion(self):
        """Test updating a global unit conversion."""
        # Create the test units
        self._create_test_units()

        # Create the test conversions
        self._create_test_unit_conversions()

        # Check the values of the first conversion
        conversion_1 = self.repository.units.read_all_global_unit_conversions()[0]
        self.assertEqual(conversion_1["from_unit_id"], self.unit_conversion_1_data["from_unit_id"])
        self.assertEqual(conversion_1["to_unit_id"], self.unit_conversion_1_data["to_unit_id"])
        self.assertEqual(conversion_1["from_unit_qty"], self.unit_conversion_1_data["from_unit_qty"])
        self.assertEqual(conversion_1["to_unit_qty"], self.unit_conversion_1_data["to_unit_qty"])

        # Update the first conversion
        self.repository.units.update_global_unit_conversion(
            unit_conversion_id=1,
            from_unit_id=2,
            to_unit_id=1,
            from_unit_qty=2,
            to_unit_qty=1,
        )

        # Check the values of the first conversion again
        conversion_1 = self.repository.units.read_all_global_unit_conversions()[0]
        self.assertEqual(conversion_1["from_unit_id"], 2)
        self.assertEqual(conversion_1["to_unit_id"], 1)
        self.assertEqual(conversion_1["from_unit_qty"], 2)
        self.assertEqual(conversion_1["to_unit_qty"], 1)

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

    def test_delete_unit_alias(self):
        """Test deleting a global unit alias."""
        # Create the test units
        self._create_test_units()

        # Check the aliases are in the database
        aliases = self.repository.units.read_unit_aliases(unit_id=self.unit_1_id)

        # Check we got the right number back
        self.assertEqual(len(aliases), 2)

        # Delete the first alias
        self.repository.units.delete_unit_alias(alias_id=1)

        # Check that only the second alias is in the database
        aliases = self.repository.units.read_unit_aliases(unit_id=self.unit_1_id)
        self.assertEqual(len(aliases), 1)
        
    def test_delete_global_unit_conversion(self):
        """Test deleting a global unit conversion."""
        # Create the test units
        self._create_test_units()

        # Create the test conversions
        self._create_test_unit_conversions()

        # Check the conversions are in the database
        conversions = self.repository.units.read_all_global_unit_conversions()

        # Check we got the right number back
        self.assertEqual(len(conversions), 2)

        # Delete the first conversion
        self.repository.units.delete_global_unit_conversion(unit_conversion_id=1)

        # Check that only the second conversion is in the database
        conversions = self.repository.units.read_all_global_unit_conversions()
        self.assertEqual(len(conversions), 1)
