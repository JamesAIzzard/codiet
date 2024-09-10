"""Tests for the UnitDBService class."""

import unittest

from codiet.tests.db.database_test_case import DatabaseTestCase
from codiet.tests.fixtures.units_test_fixtures import UnitsTestFixtures
from codiet.models.units.unit import Unit


class TestUnitDBService(DatabaseTestCase):

    def setUp(self):
        """Set up the test case.
        Pretty much all tests will need access to the test units, so these are created here.
        """
        super().setUp()

        self.units_fixtures = UnitsTestFixtures(self.db_service)

    def test_unit_id_name_map(self):
        """Checks that the unit ID to name map contains the correct entries."""
        self.units_fixtures.setup_test_units()

        # Check the length of the map is the same as the number of units
        self.assertEqual(
            len(self.db_service.units.unit_id_name_map),
            len(self.units_fixtures.test_units),
        )

        # Check that the id-name in the dict matches the map
        for unit in self.units_fixtures.test_units.values():
            self.assertEqual(self.db_service.units.unit_id_name_map.get_value(unit.id), unit.unit_name)  # type: ignore

    def test_unit_id_name_map_updates_when_new_unit_created(self):
        """Checks that the unit ID to name map updates when a new unit is created."""
        self.db_service.units.create_units(self.units_fixtures.test_units.values())

        # Check the length of the map is the same as the number of units
        original_length = len(self.db_service.units.unit_id_name_map)
        self.assertEqual(
            len(self.db_service.units.unit_id_name_map),
            len(self.units_fixtures.test_units),
        )

        # Create a new unit and add it to the database
        new_unit = Unit(
            unit_name="newunit",
            single_display_name="New Unit",
            plural_display_name="New Units",
            type="newtype",
            aliases=set(["newalias"]),
        )
        self.db_service.units.create_unit(new_unit)

        # Check that the map is updated
        self.assertIn(new_unit.id, self.db_service.units.unit_id_name_map.keys)

        # Check that the mpa got longer
        self.assertEqual(
            len(self.db_service.units.unit_id_name_map), original_length + 1
        )

    def test_units_property(self):
        """Checks that the units property returns the correct units."""
        self.units_fixtures.setup_test_units()

        # Check the property returns the correct units
        self.assertEqual(
            len(self.db_service.units.units), len(self.units_fixtures.test_units)
        )
        for unit in self.units_fixtures.test_units.values():
            self.assertIn(unit, self.db_service.units.units)

    def test_gram_unit_property(self):
        """Checks that the gram unit property returns the correct unit."""
        self.units_fixtures.setup_test_units()

        # Check the gram unit is accessible
        self.assertEqual(
            self.db_service.units.gram, self.units_fixtures.test_units["gram"]
        )

    def test_mass_units(self):
        """Checks that the mass units property returns the correct units."""
        self.units_fixtures.setup_test_units()

        # Count the number of units with mass type
        mass_units = [
            unit
            for unit in self.units_fixtures.test_units.values()
            if unit.type == "mass"
        ]
        self.assertEqual(len(mass_units), len(self.db_service.units.mass_units))

        # Check each unit is in the mass units
        for unit in mass_units:
            self.assertIn(unit, self.db_service.units.mass_units)

    def test_volume_units(self):
        """Checks that the volume units property returns the correct units."""
        self.units_fixtures.setup_test_units()

        # Count the number of units with volume type
        volume_units = [
            unit
            for unit in self.units_fixtures.test_units.values()
            if unit.type == "volume"
        ]
        self.assertEqual(len(volume_units), len(self.db_service.units.volume_units))

        # Check each unit is in the volume units
        for unit in volume_units:
            self.assertIn(unit, self.db_service.units.volume_units)

    def test_grouping_units(self):
        """Checks that the group units property returns the correct units."""
        self.units_fixtures.setup_test_units()

        # Count the number of units with grouping type
        group_units = [
            unit
            for unit in self.units_fixtures.test_units.values()
            if unit.type == "grouping"
        ]
        self.assertEqual(len(group_units), len(self.db_service.units.grouping_units))

        # Check each unit is in the group units
        for unit in group_units:
            self.assertIn(unit, self.db_service.units.grouping_units)

    def test_global_unit_conversions_property(self):
        """Checks that the global unit conversions property is returning the
        correct unit conversions."""
        self.units_fixtures.setup_test_global_unit_conversions()

        # Check the property returns the correct unit conversions
        self.assertEqual(
            len(self.db_service.units.global_unit_conversions),
            len(self.units_fixtures.test_global_unit_conversions),
        )
        for (
            unit_conversion
        ) in self.units_fixtures.test_global_unit_conversions.values():
            self.assertIn(
                unit_conversion, self.db_service.units.global_unit_conversions
            )

    def test_get_unit_by_name(self):
        """Check that we can fetch a single unit by its name."""
        self.units_fixtures.setup_test_units()

        # Check that we can fetch the kilogram unit, and that it is the correct instance.
        kg_unit = self.db_service.units.get_unit_by_name("kilogram")
        self.assertEqual(kg_unit, self.units_fixtures.test_units["kilogram"])

    def test_get_units_by_name(self):
        """Checks that we can get multiple units by their names."""
        self.units_fixtures.setup_test_units()

        # Check that we can fetch the kilogram and gram units, and that they are the correct instances.
        kg_unit, g_unit = self.db_service.units.get_units_by_name(("kilogram", "gram"))
        self.assertEqual(kg_unit, self.units_fixtures.test_units["kilogram"])
        self.assertEqual(g_unit, self.units_fixtures.test_units["gram"])

    def test_get_unit_by_id(self):
        """Checks that we can get a single unit by its ID."""
        self.units_fixtures.setup_test_units()

        # Check that we can fetch the kilogram unit by its ID, and that it is the correct instance.
        kg_unit = self.db_service.units.get_unit_by_id(self.units_fixtures.test_units["kilogram"].id)  # type: ignore
        self.assertEqual(kg_unit, self.units_fixtures.test_units["kilogram"])

    def test_get_units_by_id(self):
        """Checks that we can get multiple units by their IDs."""
        self.units_fixtures.setup_test_units()

        # Check that we can fetch the kilogram and gram units by their IDs, and that they are the correct instances.
        kg_unit, g_unit = self.db_service.units.get_units_by_id(
            (self.units_fixtures.test_units["kilogram"].id, self.units_fixtures.test_units["gram"].id)  # type: ignore
        )
        self.assertEqual(kg_unit, self.units_fixtures.test_units["kilogram"])
        self.assertEqual(g_unit, self.units_fixtures.test_units["gram"])

    def test_get_global_unit_conversion_by_units(self):
        """Checks that we can get a single unit conversion by referring to the units.
        The identity of a unit conversion is independent of the order in which the units
        are quoted, so we test both ways round.
        """
        self.units_fixtures.setup_test_global_unit_conversions()

        # Check that we can fetch the conversion by referring to the units
        gram_kilogram_uc = self.db_service.units.get_global_unit_conversion_by_units(
            self.units_fixtures.test_units["gram"],
            self.units_fixtures.test_units["kilogram"],
        )
        self.assertEqual(
            gram_kilogram_uc,
            self.units_fixtures.test_global_unit_conversions["gram-kilogram"],
        )

        # Check that we can fetch the conversion by referring to the units in reverse
        gram_kilogram_uc = self.db_service.units.get_global_unit_conversion_by_units(
            self.units_fixtures.test_units["kilogram"],
            self.units_fixtures.test_units["gram"],
        )
        self.assertEqual(
            gram_kilogram_uc,
            self.units_fixtures.test_global_unit_conversions["gram-kilogram"],
        )

    def test_get_global_unit_conversions_by_units(self):
        """Checks that we can get multiple unit conversions by units."""
        self.units_fixtures.setup_test_global_unit_conversions()

        # Check that we can fetch the conversions by referring to the units
        gram_kilogram_uc, millilitre_litre_uc = (
            self.db_service.units.get_global_unit_conversions_by_units(
                [
                    (
                        self.units_fixtures.test_units["gram"],
                        self.units_fixtures.test_units["kilogram"],
                    ),
                    (
                        self.units_fixtures.test_units["millilitre"],
                        self.units_fixtures.test_units["litre"],
                    ),
                ]
            )
        )
        self.assertEqual(
            gram_kilogram_uc,
            self.units_fixtures.test_global_unit_conversions["gram-kilogram"],
        )
        self.assertEqual(
            millilitre_litre_uc,
            self.units_fixtures.test_global_unit_conversions["millilitre-litre"],
        )

    def test_get_global_unit_conversion_by_id(self):
        """Checks that we can get a single unit conversion by its ID."""
        self.units_fixtures.setup_test_global_unit_conversions()

        # Check that we can fetch the conversion by its ID
        gram_kilogram_uc = self.db_service.units.get_global_unit_conversion_by_id(
            self.units_fixtures.test_global_unit_conversions["gram-kilogram"].id  # type: ignore
        )
        self.assertEqual(
            gram_kilogram_uc,
            self.units_fixtures.test_global_unit_conversions["gram-kilogram"],
        )

    def test_get_global_unit_conversions_by_id(self):
        """Checks that we can get multiple unit conversions by their IDs."""
        self.units_fixtures.setup_test_global_unit_conversions()

        # Check that we can fetch the conversions by their IDs
        (
            gram_kilogram_uc,
            millilitre_litre_uc,
        ) = self.db_service.units.get_global_unit_conversions_by_id(
            (self.units_fixtures.test_global_unit_conversions["gram-kilogram"].id, self.units_fixtures.test_global_unit_conversions["millilitre-litre"].id)  # type: ignore
        )
        self.assertEqual(
            gram_kilogram_uc,
            self.units_fixtures.test_global_unit_conversions["gram-kilogram"],
        )
        self.assertEqual(
            millilitre_litre_uc,
            self.units_fixtures.test_global_unit_conversions["millilitre-litre"],
        )

    def test_create_unit(self):
        """Check that we can create a single unit in the database."""
        pass  # Tested in setUp

    def test_create_units(self):
        """Check that we can create multiple units in the database."""
        pass  # Tested in setUp

    def test_create_global_unit_conversion(self):
        """Check that we can create a single global unit conversion in the database."""
        self.units_fixtures.setup_test_global_unit_conversions()

        # Check that the unit conversion is in the database
        gram_kilogram_uc = self.db_service.units.get_global_unit_conversion_by_units(
            self.units_fixtures.test_units["gram"],
            self.units_fixtures.test_units["kilogram"],
        )
        self.assertEqual(gram_kilogram_uc, self.units_fixtures.test_global_unit_conversions["gram-kilogram"])

    def test_create_global_unit_conversions(self):
        """Check that we can create multiple global unit conversions in the database."""
        self.units_fixtures.setup_test_global_unit_conversions()

        # Check that the unit conversions are in the database
        gram_kilogram_uc, millilitre_litre_uc = (
            self.db_service.units.get_global_unit_conversions_by_units(
                [
                    (
                        self.units_fixtures.test_units["gram"],
                        self.units_fixtures.test_units["kilogram"],
                    ),
                    (
                        self.units_fixtures.test_units["millilitre"],
                        self.units_fixtures.test_units["litre"],
                    ),
                ]
            )
        )
        self.assertEqual(gram_kilogram_uc, self.units_fixtures.test_global_unit_conversions["gram-kilogram"])
        self.assertEqual(millilitre_litre_uc, self.units_fixtures.test_global_unit_conversions["millilitre-litre"])

    @unittest.skip("Not yet implemented")
    def test_create_ingredient_unit_conversion(self):
        """Check that we can create a single ingredient unit conversion in the database."""
        raise NotImplementedError

    @unittest.skip("Not yet implemented")
    def test_create_ingredient_unit_conversions(self):
        """Check that we can create multiple ingredient unit conversions in the database."""
        raise NotImplementedError

    def test_read_all_units(self):
        """Check we can get the correct collection of all units from the database."""
        self.units_fixtures.setup_test_units()

        # Read the units from the database
        units = self.db_service.units.read_all_units()

        # Check that the units are the same
        self.assertCountEqual(units, self.units_fixtures.test_units.values())

    def test_read_all_global_unit_conversions(self):
        """Check we can get the correct collection of global unit conversions from the database."""
        self.units_fixtures.setup_test_global_unit_conversions()

        # Read the unit conversions from the database
        unit_conversions = self.db_service.units.read_all_global_unit_conversions()

        # Check that the unit conversions are the same
        self.assertCountEqual(unit_conversions, self.units_fixtures.test_global_unit_conversions.values())

    @unittest.skip("Not yet implemented")
    def test_read_ingredient_unit_conversions(self):
        """Check we can read an ingredient's unit conversions from the database."""
        raise NotImplementedError

    def test_update_unit(self):
        """Check that we can update a single existing unit in the database."""
        self.units_fixtures.setup_test_units()

        # Grab the kilogram unit and check its properties
        kg_unit = self.db_service.units.get_unit_by_name("kilogram")
        self.assertEqual(kg_unit.single_display_name, "kg")
        self.assertEqual(kg_unit.plural_display_name, "kg")
        self.assertEqual(kg_unit.type, "mass")
        self.assertEqual(len(kg_unit.aliases), 1)
        self.assertIn("kgs", kg_unit.aliases)

        # Modify it (modify private variables because we don't provide setters right now)
        kg_unit._single_display_name = "modifiedkg"
        kg_unit._plural_display_name = "modifiedkgs"
        kg_unit._type = "modifiedtype"
        kg_unit._aliases = set(["modifiedkgalias"])

        # Update the unit
        self.db_service.units.update_unit(kg_unit)

        # Reread the unit from the database
        updated_kg = self.db_service.units.get_unit_by_name("kilogram")

        # Check that the unit is updated
        self.assertEqual(updated_kg, kg_unit)
        self.assertEqual(updated_kg.single_display_name, "modifiedkg")
        self.assertEqual(updated_kg.plural_display_name, "modifiedkgs")
        self.assertEqual(updated_kg.type, "modifiedtype")
        self.assertEqual(updated_kg.aliases, set(["modifiedkgalias"]))

    def test_update_units(self):
        """Check that we can update multiple existing units in the database."""
        self.units_fixtures.setup_test_units()

        # Grab the kilogram and gram units and check their properties
        kg_unit, g_unit = self.db_service.units.get_units_by_name(("kilogram", "gram"))

        self.assertEqual(kg_unit.single_display_name, "kg")
        self.assertEqual(kg_unit.plural_display_name, "kg")
        self.assertEqual(kg_unit.type, "mass")
        self.assertEqual(len(kg_unit.aliases), 1)
        self.assertIn("kgs", kg_unit.aliases)

        self.assertEqual(g_unit.single_display_name, "g")
        self.assertEqual(g_unit.plural_display_name, "g")
        self.assertEqual(g_unit.type, "mass")
        self.assertEqual(len(g_unit.aliases), 0)

        # Modify them (modify private variables because we don't provide setters right now)
        kg_unit._single_display_name = "modifiedkg"
        kg_unit._plural_display_name = "modifiedkgs"
        kg_unit._type = "modifiedtype"
        kg_unit._aliases = set(["modifiedkgalias"])

        g_unit._single_display_name = "modifiedg"
        g_unit._plural_display_name = "modifiedgs"
        g_unit._type = "modifiedtype"
        g_unit._aliases = set(["modifiedgalias"])

        # Update the units
        self.db_service.units.update_units([kg_unit, g_unit])

        # Reread the units from the database
        updated_kg, updated_g = self.db_service.units.get_units_by_name(
            ("kilogram", "gram")
        )

        # Check that the units are updated
        self.assertEqual(updated_kg, kg_unit)
        self.assertEqual(updated_kg.single_display_name, "modifiedkg")
        self.assertEqual(updated_kg.plural_display_name, "modifiedkgs")
        self.assertEqual(updated_kg.type, "modifiedtype")
        self.assertEqual(updated_kg.aliases, set(["modifiedkgalias"]))

        self.assertEqual(updated_g, g_unit)
        self.assertEqual(updated_g.single_display_name, "modifiedg")
        self.assertEqual(updated_g.plural_display_name, "modifiedgs")
        self.assertEqual(updated_g.type, "modifiedtype")
        self.assertEqual(updated_g.aliases, set(["modifiedgalias"]))

    def test_update_global_unit_conversion(self):
        """Check that we can update a global unit conversion in the database."""
        self.units_fixtures.setup_test_global_unit_conversions()

        # Grab the gram-kilogram unit conversion and check its properties
        gram_kilogram_uc = self.db_service.units.get_global_unit_conversion_by_units(
            self.units_fixtures.test_units["gram"],
            self.units_fixtures.test_units["kilogram"],
        )
        self.assertEqual(gram_kilogram_uc.from_unit_qty, 1000)
        self.assertEqual(gram_kilogram_uc.to_unit_qty, 1)

        # Modify it (modify private variables because we don't provide setters right now)
        gram_kilogram_uc._from_unit_qty = 2000
        gram_kilogram_uc._to_unit_qty = 2

        # Update the unit conversion
        self.db_service.units.update_global_unit_conversion(gram_kilogram_uc)

        # Reread the unit conversion from the database
        updated_gram_kilogram_uc = (
            self.db_service.units.get_global_unit_conversion_by_units(
                self.units_fixtures.test_units["gram"],
                self.units_fixtures.test_units["kilogram"],
            )
        )

        # Check that the unit conversion is updated
        self.assertEqual(updated_gram_kilogram_uc, gram_kilogram_uc)
        self.assertEqual(updated_gram_kilogram_uc.from_unit_qty, 2000)
        self.assertEqual(updated_gram_kilogram_uc.to_unit_qty, 2)

    def test_update_global_unit_conversions(self):
        """Check that we can update multiple global unit conversions in the database."""
        self.units_fixtures.setup_test_global_unit_conversions()

        # Grab the gram-kilogram and millilitre-litre unit conversions and check their properties
        gram_kilogram_uc, millilitre_litre_uc = (
            self.db_service.units.get_global_unit_conversions_by_units(
                [
                    (
                        self.units_fixtures.test_units["gram"],
                        self.units_fixtures.test_units["kilogram"],
                    ),
                    (
                        self.units_fixtures.test_units["millilitre"],
                        self.units_fixtures.test_units["litre"],
                    ),
                ]
            )
        )
        self.assertEqual(gram_kilogram_uc.from_unit_qty, 1000)
        self.assertEqual(gram_kilogram_uc.to_unit_qty, 1)
        self.assertEqual(millilitre_litre_uc.from_unit_qty, 1000)
        self.assertEqual(millilitre_litre_uc.to_unit_qty, 1)

        # Modify them (modify private variables because we don't provide setters right now)
        gram_kilogram_uc._from_unit_qty = 2000
        gram_kilogram_uc._to_unit_qty = 2

        millilitre_litre_uc._from_unit_qty = 2000
        millilitre_litre_uc._to_unit_qty = 2

        # Update the unit conversions
        self.db_service.units.update_global_unit_conversions(
            [gram_kilogram_uc, millilitre_litre_uc]
        )

        # Reread the unit conversions from the database
        updated_gram_kilogram_uc, updated_millilitre_litre_uc = (
            self.db_service.units.get_global_unit_conversions_by_units(
                [
                    (
                        self.units_fixtures.test_units["gram"],
                        self.units_fixtures.test_units["kilogram"],
                    ),
                    (
                        self.units_fixtures.test_units["millilitre"],
                        self.units_fixtures.test_units["litre"],
                    ),
                ]
            )
        )

        # Check that the unit conversions are updated
        self.assertEqual(updated_gram_kilogram_uc, gram_kilogram_uc)
        self.assertEqual(updated_gram_kilogram_uc.from_unit_qty, 2000)
        self.assertEqual(updated_gram_kilogram_uc.to_unit_qty, 2)

        self.assertEqual(updated_millilitre_litre_uc, millilitre_litre_uc)
        self.assertEqual(updated_millilitre_litre_uc.from_unit_qty, 2000)
        self.assertEqual(updated_millilitre_litre_uc.to_unit_qty, 2)

    @unittest.skip("Not yet implemented")
    def test_update_ingredient_unit_conversion(self):
        """Checks that we can update an ingredient unit conversion in the database."""
        raise NotImplementedError

    @unittest.skip("Not yet implemented")
    def test_update_ingredient_unit_conversions(self):
        """Checks that we can update multiple ingredient unit conversions in the database."""
        raise NotImplementedError

    def test_delete_unit(self):
        """Checks that we can delete a unit from the database.
        Also confirms the unit is no longer present in the other properties and read methods.
        """
        self.units_fixtures.setup_test_units()

        # Grab the kilogram unit
        kg_unit = self.db_service.units.get_unit_by_name("kilogram")

        # Check the unit was fetched correctly
        self.assertEqual(kg_unit, self.units_fixtures.test_units["kilogram"])

        # Delete the unit
        self.db_service.units.delete_unit(kg_unit)

        # Assert we get a key error when trying to get the unit
        with self.assertRaises(KeyError):
            self.db_service.units.get_unit_by_name("kilogram")

        # Check the unit is no longer in the units property
        self.assertNotIn(kg_unit, self.db_service.units.units)

        # Check the unit is no longer in the unit_id_name_map
        self.assertNotIn(kg_unit.id, self.db_service.units.unit_id_name_map.keys)
        self.assertNotIn(
            kg_unit.unit_name, self.db_service.units.unit_id_name_map.values
        )

        # Check read_all_units no longer returns the unit
        units = self.db_service.units.read_all_units()
        self.assertNotIn(kg_unit, units)

    def test_delete_units(self):
        """Checks that we can delete multiple units from the database.
        Also confirms the units are no longer present in the other properties and read methods.
        """
        self.units_fixtures.setup_test_units()

        # Grab the kilogram and gram units
        kg_unit, g_unit = self.db_service.units.get_units_by_name(("kilogram", "gram"))

        # Check the units were fetched correctly
        self.assertEqual(kg_unit, self.units_fixtures.test_units["kilogram"])
        self.assertEqual(g_unit, self.units_fixtures.test_units["gram"])

        # Delete the units
        self.db_service.units.delete_units([kg_unit, g_unit])

        # Check the units are no longer in the units property
        self.assertNotIn(kg_unit, self.db_service.units.units)
        self.assertNotIn(g_unit, self.db_service.units.units)

        # Check the units are no longer in the unit_id_name_map
        self.assertNotIn(kg_unit.id, self.db_service.units.unit_id_name_map.keys)
        self.assertNotIn(
            kg_unit.unit_name, self.db_service.units.unit_id_name_map.values
        )
        self.assertNotIn(g_unit.id, self.db_service.units.unit_id_name_map.keys)
        self.assertNotIn(
            g_unit.unit_name, self.db_service.units.unit_id_name_map.values
        )

        # Check read_all_units no longer returns the units
        units = self.db_service.units.read_all_units()
        self.assertNotIn(kg_unit, units)
        self.assertNotIn(g_unit, units)

    def test_delete_global_unit_conversion(self):
        """Checks that we can delete a global unit conversion from the database.
        Also confirms the unit conversion is no longer present in the other properties and read methods.
        """
        self.units_fixtures.setup_test_global_unit_conversions()

        # Grab the gram-kilogram unit conversion
        gram_kilogram_uc = self.db_service.units.get_global_unit_conversion_by_units(
            self.units_fixtures.test_units["gram"],
            self.units_fixtures.test_units["kilogram"],
        )

        # Check the unit conversion was fetched correctly
        self.assertEqual(gram_kilogram_uc, self.units_fixtures.test_global_unit_conversions["gram-kilogram"])

        # Delete the unit conversion
        self.db_service.units.delete_global_unit_conversion(gram_kilogram_uc)

        # Check the unit conversion is no longer in the global_unit_conversions property
        self.assertNotIn(
            gram_kilogram_uc, self.db_service.units.global_unit_conversions
        )

        # Check read_all_global_unit_conversions no longer returns the unit conversion
        unit_conversions = self.db_service.units.read_all_global_unit_conversions()
        self.assertNotIn(gram_kilogram_uc, unit_conversions)

    def test_delete_global_unit_conversions(self):
        """Checks that we can delete multiple global unit conversions from the database.
        Also confirms the unit conversions are no longer present in the other properties and read methods.
        """
        self.units_fixtures.setup_test_global_unit_conversions()

        # Grab the gram-kilogram and millilitre-litre unit conversions
        gram_kilogram_uc, millilitre_litre_uc = (
            self.db_service.units.get_global_unit_conversions_by_units(
                [
                    (
                        self.units_fixtures.test_units["gram"],
                        self.units_fixtures.test_units["kilogram"],
                    ),
                    (
                        self.units_fixtures.test_units["millilitre"],
                        self.units_fixtures.test_units["litre"],
                    ),
                ]
            )
        )

        # Check the unit conversions were fetched correctly
        self.assertEqual(gram_kilogram_uc, self.units_fixtures.test_global_unit_conversions["gram-kilogram"])
        self.assertEqual(millilitre_litre_uc, self.units_fixtures.test_global_unit_conversions["millilitre-litre"])

        # Delete the unit conversions
        self.db_service.units.delete_global_unit_conversions(
            [gram_kilogram_uc, millilitre_litre_uc]
        )

        # Check the unit conversions are no longer in the global_unit_conversions property
        self.assertNotIn(
            gram_kilogram_uc, self.db_service.units.global_unit_conversions
        )
        self.assertNotIn(
            millilitre_litre_uc, self.db_service.units.global_unit_conversions
        )

        # Check read_all_global_unit_conversions no longer returns the unit conversions
        unit_conversions = self.db_service.units.read_all_global_unit_conversions()
        self.assertNotIn(gram_kilogram_uc, unit_conversions)
        self.assertNotIn(millilitre_litre_uc, unit_conversions)

    @unittest.skip("Not yet implemented")
    def test_delete_ingredient_unit_conversion(self):
        """Checks that we can delete an ingredient unit conversion from the database."""
        raise NotImplementedError

    @unittest.skip("Not yet implemented")
    def test_delete_ingredient_unit_conversions(self):
        """Checks that we can delete multiple ingredient unit conversions from the database."""
        raise NotImplementedError
