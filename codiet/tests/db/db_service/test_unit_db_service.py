from unittest.mock import Mock
from codiet.tests.db.database_test_case import DatabaseTestCase
from codiet.db_population.units import read_units_from_json, read_global_unit_conversions_from_json
from codiet.models.units.unit import Unit
from codiet.models.units.ingredient_unit_conversion import IngredientUnitConversion

class TestUnitDBService(DatabaseTestCase):

    def setUp(self):
        super().setUp()

        # Create a mock test ingredient with an ID
        self.mock_ingredient = Mock()
        self.mock_ingredient.id = 1

    def _populate_unit_conversions(self):
        """Populates the database with unit conversions."""
        # Create the units
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Create the unit conversions
        unit_conversions_from_json = read_global_unit_conversions_from_json(
            global_units=self.db_service.units.units
        )
        self.db_service.units.create_global_unit_conversions(unit_conversions_from_json)

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
        self.db_service.units.create_unit(new_unit)

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

    def test_global_unit_conversions(self):
        """Checks that the global unit conversions are correct."""
        self._populate_unit_conversions()

        # Check the length of the global unit conversions is the same as the number of unit conversions
        unit_conversions_from_json = read_global_unit_conversions_from_json()
        self.assertEqual(len(unit_conversions_from_json), len(self.db_service.units.global_unit_conversions))

        # Check each unit conversion is in the global unit conversions
        for unit_conversion in unit_conversions_from_json:
            self.assertIn(unit_conversion, self.db_service.units.global_unit_conversions)

    def test_get_unit_by_name(self):
        """Checks that we can get a single unit by its name."""
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        kg_unit = self.db_service.units.get_unit_by_name("kilogram")
        self.assertEqual(kg_unit.unit_name, "kilogram")

    def test_get_units_by_name(self):
        """Checks that we can get multiple units by their names."""
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        kg_unit, g_unit = self.db_service.units.get_units_by_name(("kilogram", "gram"))
        self.assertEqual(kg_unit.unit_name, "kilogram")
        self.assertEqual(g_unit.unit_name, "gram")

    def test_get_unit_by_id(self):
        """Checks that we can get a single unit by its ID."""
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        kg_unit = self.db_service.units.get_unit_by_name("kilogram")
        kg_unit_by_id = self.db_service.units.get_unit_by_id(kg_unit.id)  # type: ignore
        self.assertEqual(kg_unit_by_id.unit_name, "kilogram")

    def test_get_units_by_id(self):
        """Checks that we can get multiple units by their IDs."""
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        kg_unit, g_unit = self.db_service.units.get_units_by_name(("kilogram", "gram"))
        kg_unit_by_id, g_unit_by_id = self.db_service.units.get_units_by_id([kg_unit.id, g_unit.id])  # type: ignore
        self.assertEqual(kg_unit.id, kg_unit_by_id.id)
        self.assertEqual(g_unit.id, g_unit_by_id.id)

    def test_get_global_unit_conversion_by_units(self):
        """Checks that we can get a single unit conversion by units."""
        self._populate_unit_conversions()

        kg_unit, g_unit = self.db_service.units.get_units_by_name(("kilogram", "gram"))
        g_kg_conversion = self.db_service.units.get_global_unit_conversion_by_units(kg_unit, g_unit)
        self.assertIn(g_unit, g_kg_conversion.units)
        self.assertIn(kg_unit, g_kg_conversion.units)

    def test_get_global_unit_conversions_by_units(self):
        """Checks that we can get multiple unit conversions by units."""
        self._populate_unit_conversions()

        kg_unit, g_unit = self.db_service.units.get_units_by_name(("kilogram", "gram"))
        L_unit, ml_unit = self.db_service.units.get_units_by_name(("litre", "millilitre"))
        conversions = self.db_service.units.get_global_unit_conversions_by_units(((kg_unit, g_unit), (L_unit, ml_unit)))
        g_kg_conversion, ml_L_conversion = conversions

        self.assertIn(g_unit, g_kg_conversion.units)
        self.assertIn(kg_unit, g_kg_conversion.units)
        self.assertIn(L_unit, ml_L_conversion.units)
        self.assertIn(ml_unit, ml_L_conversion.units)

    def test_get_global_unit_conversion_by_id(self):
        """Checks that we can get a single unit conversion by its ID."""
        self._populate_unit_conversions()

        kg_unit, g_unit = self.db_service.units.get_units_by_name(("kilogram", "gram"))
        g_kg_conversion = self.db_service.units.get_global_unit_conversion_by_units(kg_unit, g_unit)
        g_kg_conversion_by_id = self.db_service.units.get_global_unit_conversion_by_id(g_kg_conversion.id)  # type: ignore
        self.assertEqual(g_kg_conversion_by_id, g_kg_conversion)

    def test_get_global_unit_conversions_by_id(self):
        """Checks that we can get multiple unit conversions by their IDs."""
        self._populate_unit_conversions()

        kg_unit, g_unit = self.db_service.units.get_units_by_name(("kilogram", "gram"))
        L_unit, ml_unit = self.db_service.units.get_units_by_name(("litre", "millilitre"))
        conversions = self.db_service.units.get_global_unit_conversions_by_units(((kg_unit, g_unit), (L_unit, ml_unit)))
        g_kg_conversion, ml_L_conversion = conversions
        
        conversions_by_id = self.db_service.units.get_global_unit_conversions_by_id([g_kg_conversion.id, ml_L_conversion.id])  # type: ignore
        g_kg_conversion_by_id, ml_L_conversion_by_id = conversions_by_id

        self.assertEqual(g_kg_conversion_by_id, g_kg_conversion)
        self.assertEqual(ml_L_conversion_by_id, ml_L_conversion)
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
        self._populate_unit_conversions()

        # Read the unit conversions from the database
        unit_conversions = self.db_service.units.read_all_global_unit_conversions()

        # Check that the unit conversions are the same
        self.assertEqual(unit_conversions, read_global_unit_conversions_from_json())

        # Check that all unit conversions are persisted
        for unit_conversion in unit_conversions:
            self.assertTrue(unit_conversion.is_persisted)

    def test_create_and_read_ingredient_unit_conversions(self):
        """Check we can read and write ingredient unit conversions to the database."""
        # Populate the global units
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Grab a couple of units
        kg, g = self.db_service.units.get_units_by_name(("kilogram", "gram"))

        # Create an ingredient unit conversion instance
        ingredient_unit_conversion = IngredientUnitConversion(
            ingredient=self.mock_ingredient,
            from_unit=kg,
            to_unit=g,
            from_unit_qty=1,
            to_unit_qty=1000
        )

        # Create the ingredient unit conversion
        iuc = self.db_service.units.create_ingredient_unit_conversion(ingredient_unit_conversion)

        # Read the ingredient unit conversions from the database
        ingredient_unit_conversions = self.db_service.units.read_ingredient_unit_conversions(
            self.mock_ingredient
        )

        # Check that the ingredient unit conversions are the same
        self.assertEqual(ingredient_unit_conversions, tuple([ingredient_unit_conversion]))

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
        self.db_service.units.update_unit(kg_unit)

        # Read the units from the database
        updated_kg = self.db_service.units.get_unit_by_name("kilogram")

        # Check that the unit is updated
        self.assertEqual(updated_kg, kg_unit)
        self.assertEqual(updated_kg.single_display_name, "modifiedkg")
        self.assertEqual(updated_kg.plural_display_name, "modifiedkgs")
        self.assertEqual(updated_kg.type, "modifiedtype")
        self.assertEqual(updated_kg.aliases, set(["modifiedkgalias"]))

    def test_update_global_unit_conversions(self):
        """Checks that we can update a unit conversion in the database.
        Also confirms the caching updates correctly.
        """
        pass # Currently, unit conversions are immutable

    def test_update_ingredient_unit_conversion(self):
        """Checks that we can update an ingredient unit conversion in the database."""
        # Populate the global units
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Grab a couple of units
        kg, g = self.db_service.units.get_units_by_name(("kilogram", "gram"))

        # Create an ingredient unit conversion instance
        ingredient_unit_conversion = IngredientUnitConversion(
            ingredient=self.mock_ingredient,
            from_unit=kg,
            to_unit=g,
            from_unit_qty=1,
            to_unit_qty=1000
        )

        # Create the ingredient unit conversion
        iuc = self.db_service.units.create_ingredient_unit_conversion(ingredient_unit_conversion)

        # Check the properties were set correctly
        self.assertEqual(iuc.from_unit_qty, 1)
        self.assertEqual(iuc.to_unit_qty, 1000)

        # Update the ingredient unit conversion
        iuc.from_unit_qty = 2
        iuc.to_unit_qty = 2000

        # Update the ingredient unit conversion
        self.db_service.units.update_ingredient_unit_conversion(iuc)

        # Read the ingredient unit conversions from the database
        ingredient_unit_conversions = self.db_service.units.read_ingredient_unit_conversions(
            self.mock_ingredient
        )

        # Check that the ingredient unit conversions are the same
        self.assertEqual(ingredient_unit_conversions, tuple([iuc]))

    def test_delete_ingredient_unit_conversion(self):
        """Checks that we can delete an ingredient unit conversion from the database."""
        # Populate the global units
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Grab a couple of units
        kg, g = self.db_service.units.get_units_by_name(("kilogram", "gram"))

        # Create an ingredient unit conversion instance
        ingredient_unit_conversion = IngredientUnitConversion(
            ingredient=self.mock_ingredient,
            from_unit=kg,
            to_unit=g,
            from_unit_qty=1,
            to_unit_qty=1000
        )

        # Create the ingredient unit conversion
        iuc = self.db_service.units.create_ingredient_unit_conversion(ingredient_unit_conversion)

        # Read it to check it is there
        ingredient_unit_conversions = self.db_service.units.read_ingredient_unit_conversions(
            self.mock_ingredient
        )
        # Check that the ingredient unit conversions are the same
        self.assertEqual(ingredient_unit_conversions, tuple([iuc]))

        # Delete the ingredient unit conversion
        self.db_service.units.delete_ingredient_unit_conversion(iuc)

        # Read the ingredient unit conversions from the database
        ingredient_unit_conversions = self.db_service.units.read_ingredient_unit_conversions(
            self.mock_ingredient
        )

        # Check that the ingredient unit conversions are empty
        self.assertEqual(ingredient_unit_conversions, tuple())

    def test_delete_units(self):
        """Checks that we can delete a unit from the database.
        Also confirms the caching updates correctly.
        """
        units_from_json = read_units_from_json()
        self.db_service.units.create_units(units_from_json)

        # Grab the kilogram unit
        kg_unit = self.db_service.units.get_unit_by_name("kilogram")

        # Delete the unit
        self.db_service.units.delete_unit(kg_unit)

        # Assert we get a key error when trying to get the unit
        with self.assertRaises(KeyError):
            self.db_service.units.get_unit_by_name("kilogram")

        self.assertNotIn(kg_unit, self.db_service.units.units)
