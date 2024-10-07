from codiet.tests import BaseCodietTest


class BaseUnitSystemTest(BaseCodietTest):

    def setUp(self) -> None:
        super().setUp()


class TestAvailableUnits(BaseUnitSystemTest):

    def test_init_with_only_mass_units(self):
        unit_system = self.quantities_factory.create_unit_system()

        self.assertTrue(len(unit_system.available_units) > 1)
        for unit in unit_system.available_units:
            self.assertTrue(unit.type == "mass")

    def test_gram_is_immediately_available(self):
        unit_system = self.quantities_factory.create_unit_system()

        self.assertIn(
            self.singleton_register.get_unit("gram"), unit_system.available_units
        )

    def test_millilitre_is_not_immediately_available(self):
        unit_system = self.quantities_factory.create_unit_system()

        self.assertNotIn(
            self.singleton_register.get_unit("millilitre"), unit_system.available_units
        )

    def test_millilitre_becomes_available_with_conversion(self):
        unit_system = self.quantities_factory.create_unit_system()

        unit_system.add_entity_unit_conversion(
            self.quantities_factory.create_unit_conversion(
                from_unit_name="gram",
                from_unit_quantity=1000,
                to_unit_name="millilitre",
                to_unit_quantity=1100,
            )
        )

        self.assertIn(
            self.singleton_register.get_unit("millilitre"), unit_system.available_units
        )

class TestCheckUnitAvailable(BaseUnitSystemTest):

    def test_gram_immediately_available(self):
        unit_system = self.quantities_factory.create_unit_system()

        self.assertTrue(unit_system.check_unit_available("gram"))

    def test_millilitre_not_immediately_available(self):
        unit_system = self.quantities_factory.create_unit_system()

        self.assertFalse(unit_system.check_unit_available("millilitre"))

    def test_millilitre_available_with_correct_conversion(self):
        unit_system = self.quantities_factory.create_unit_system()

        unit_system.add_entity_unit_conversion(
            self.quantities_factory.create_unit_conversion(
                from_unit_name="gram",
                from_unit_quantity=1000,
                to_unit_name="millilitre",
                to_unit_quantity=1100,
            )
        )

        self.assertTrue(unit_system.check_unit_available("millilitre"))

class TestCanConvertUnits(BaseUnitSystemTest):
    
        def test_gram_to_kilogram(self):
            unit_system = self.quantities_factory.create_unit_system()
    
            self.assertTrue(unit_system.can_convert_units(
                self.singleton_register.get_unit("gram"),
                self.singleton_register.get_unit("kilogram"),
            ))