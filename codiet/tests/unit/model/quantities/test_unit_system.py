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
    
    def test_can_convert_gram_to_kg_by_default(self):
        unit_system = self.quantities_factory.create_unit_system()

        self.assertTrue(unit_system.can_convert_units(
            from_unit_name="gram",
            to_unit_name="kilogram",
        ))

    def test_can_only_convert_gram_to_ml_with_conversion(self):
        unit_system = self.quantities_factory.create_unit_system()

        self.assertFalse(unit_system.can_convert_units(
            from_unit_name="gram",
            to_unit_name="millilitre",
        ))

        unit_system.add_entity_unit_conversion(
            self.quantities_factory.create_unit_conversion(
                from_unit_name="gram",
                from_unit_quantity=1000,
                to_unit_name="millilitre",
                to_unit_quantity=1100,
            )
        )

        self.assertTrue(unit_system.can_convert_units(
            from_unit_name="gram",
            to_unit_name="millilitre",
        ))

    def test_loose_access_to_conversion_if_removed(self):
        unit_system = self.quantities_factory.create_unit_system()

        unit_conversion = self.quantities_factory.create_unit_conversion(
            from_unit_name="gram",
            from_unit_quantity=1000,
            to_unit_name="millilitre",
            to_unit_quantity=1100,
        )

        unit_system.add_entity_unit_conversion(unit_conversion)

        self.assertTrue(unit_system.can_convert_units(
            from_unit_name="gram",
            to_unit_name="millilitre",
        ))

        unit_system.remove_entity_unit_conversion(unit_conversion)

        self.assertFalse(unit_system.can_convert_units(
            from_unit_name="gram",
            to_unit_name="millilitre",
        ))

class TestConvertQuantity(BaseUnitSystemTest):

    def test_can_convert_g_to_kg_by_default(self):
        unit_system = self.quantities_factory.create_unit_system()

        quantity = self.quantities_factory.create_quantity(
            unit_name="gram",
            value=1000,
        )

        converted_quantity = unit_system.convert_quantity(
            quantity=quantity,
            to_unit=self.singleton_register.get_unit("kilogram"),
        )

        self.assertEqual(converted_quantity.value, 1)

    def test_can_convert_g_to_ml_with_conversion(self):
        unit_system = self.quantities_factory.create_unit_system()

        unit_system.add_entity_unit_conversion(
            self.quantities_factory.create_unit_conversion(
                from_unit_name="gram",
                from_unit_quantity=1000,
                to_unit_name="millilitre",
                to_unit_quantity=1100,
            )
        )

        quantity = self.quantities_factory.create_quantity(
            unit_name="gram",
            value=1000,
        )

        converted_quantity = unit_system.convert_quantity(
            quantity=quantity,
            to_unit=self.singleton_register.get_unit("millilitre"),
        )

        self.assertEqual(converted_quantity.value, 1100)


        