from codiet.tests import BaseCodietTest
from codiet.tests.fixtures import QuantitiesTestFixtures
from codiet.model.quantities import UnitSystem, UnitConversion, Quantity

class BaseUnitSystemTest(BaseCodietTest):
    
        def setUp(self) -> None:
            super().setUp()
            self.quantities_fixtures = QuantitiesTestFixtures.get_instance()

class TestConstructor(BaseUnitSystemTest):

    def test_construct_with_no_args(self):
        unit_system = UnitSystem()

        self.assertIsInstance(unit_system, UnitSystem)
        self.assertEqual(len(unit_system.entity_unit_conversions), 0)

    def test_construct_with_entity_unit_conversions(self):
        gram_millilitre = UnitConversion(
            (
                Quantity(self.quantities_fixtures.get_unit("gram"), 1),
                Quantity(self.quantities_fixtures.get_unit("millilitre"), 1)
            )
        )
        unit_system = UnitSystem([gram_millilitre])

        self.assertIsInstance(unit_system, UnitSystem)
        self.assertEqual(len(unit_system.entity_unit_conversions), 1)

class TestAvailableUnits(BaseUnitSystemTest):
    
    def test_get_mass_units_only_without_additional_conversions(self):
        unit_system = UnitSystem()

        mass_units = unit_system.available_units
        for unit in mass_units:
            self.assertEqual(unit.type, "mass")

    def test_get_fluid_units_with_mass_fluid_conversion(self):
        unit_system = UnitSystem()

        gram_millilitre = self.quantities_fixtures.get_unit_conversion_by_unit_names(("gram", "millilitre"))
        unit_system.add_entity_unit_conversion(gram_millilitre)

        millilitre = self.quantities_fixtures.get_unit("millilitre")
        self.assertIn(millilitre, unit_system.available_units)

class TestAddEntityUnitConversion(BaseUnitSystemTest):

    def test_add_entity_unit_conversion(self):
        unit_system = UnitSystem()

        assert len(unit_system.entity_unit_conversions) == 0

        gram_millilitre = self.quantities_fixtures.get_unit_conversion_by_unit_names(("gram", "millilitre"))
        unit_system.add_entity_unit_conversion(gram_millilitre)

        self.assertEqual(len(unit_system.entity_unit_conversions), 1)
        self.assertIn(gram_millilitre, unit_system.entity_unit_conversions)

    def test_cant_add_same_conversion_twice(self):
        unit_system = UnitSystem()

        gram_millilitre = self.quantities_fixtures.get_unit_conversion_by_unit_names(("gram", "millilitre"))
        unit_system.add_entity_unit_conversion(gram_millilitre)

        with self.assertRaises(ValueError):
            unit_system.add_entity_unit_conversion(gram_millilitre)

class TestRemoveEntityUnitConversion(BaseUnitSystemTest):
    
    def test_remove_entity_unit_conversion(self):
        unit_system = UnitSystem()

        gram_millilitre = self.quantities_fixtures.get_unit_conversion_by_unit_names(("gram", "millilitre"))
        unit_system.add_entity_unit_conversion(gram_millilitre)

        self.assertEqual(len(unit_system.entity_unit_conversions), 1)

        unit_system.remove_entity_unit_conversion(gram_millilitre)

        self.assertEqual(len(unit_system.entity_unit_conversions), 0)

    def test_cant_remove_nonexistent_conversion(self):
        unit_system = UnitSystem()

        gram_millilitre = self.quantities_fixtures.get_unit_conversion_by_unit_names(("gram", "millilitre"))

        with self.assertRaises(ValueError):
            unit_system.remove_entity_unit_conversion(gram_millilitre)

class TestCanConvertUnits(BaseUnitSystemTest):

    def test_cant_convert_mass_to_fluid_until_conversion_added(self):
        unit_system = UnitSystem()

        gram = self.quantities_fixtures.get_unit("gram")
        millilitre = self.quantities_fixtures.get_unit("millilitre")

        self.assertFalse(unit_system.can_convert_units(gram, millilitre))

        unit_system.add_entity_unit_conversion(
            self.quantities_fixtures.get_unit_conversion_by_unit_names(("gram", "millilitre"))
        )

        self.assertTrue(unit_system.can_convert_units(gram, millilitre))

class TestConvertQuantity(BaseUnitSystemTest):
    
    def test_convert_quantity(self):
        unit_system = UnitSystem()

        gram = self.quantities_fixtures.get_unit("gram")
        kilogram = self.quantities_fixtures.get_unit("kilogram")

        quantity = Quantity(gram, 1000)
        converted_quantity = unit_system.convert_quantity(quantity, kilogram)

        self.assertEqual(converted_quantity.unit, kilogram)
        self.assertEqual(converted_quantity.value, 1)

    def test_can_convert_quantity_after_conversion_is_added(self):
        unit_system = UnitSystem()

        gram = self.quantities_fixtures.get_unit("gram")
        millilitre = self.quantities_fixtures.get_unit("millilitre")

        quantity = Quantity(gram, 1000)

        with self.assertRaises(ValueError):
            unit_system.convert_quantity(quantity, millilitre)

        unit_system.add_entity_unit_conversion(
            self.quantities_fixtures.get_unit_conversion_by_unit_names(("gram", "millilitre"))
        )

        converted_quantity = unit_system.convert_quantity(quantity, millilitre)

        self.assertEqual(converted_quantity.unit, millilitre)
        self.assertEqual(converted_quantity.value, 1000)