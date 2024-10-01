from codiet.tests import BaseCodietTest
from codiet.tests.custom_assertions import assertDictValuesIdentical
from codiet.model.quantities import Unit, UnitConversion

class BaseSingletonRegistryTest(BaseCodietTest):
    
    def setUp(self) -> None:
        super().setUp()       

class TestConstructor(BaseSingletonRegistryTest):

    def test_can_init(self):
        singleton_registry = SingletonRegistry()
        self.assertIsInstance(singleton_registry, SingletonRegistry)

class TestGetUnit(BaseSingletonRegistryTest):

    def test_can_get_unit(self):
        singleton_registry = SingletonRegistry()
        singleton_unit = singleton_registry.get_unit("millilitre")
        fixture_unit = self.fixture_manager.quantities_fixtures.get_unit("millilitre")
        self.assertIsInstance(singleton_unit, Unit)
        self.assertIs(singleton_unit, fixture_unit)

class TestGetGlobalUnitConversion(BaseSingletonRegistryTest):

    def test_can_get_global_unit_conversion(self):
        singleton_registry = SingletonRegistry()
        singleton_unit_conversion = singleton_registry.get_global_unit_conversion(frozenset(["millilitre", "litre"]))
        fixture_unit_conversion = self.fixture_manager.quantities_fixtures.get_global_unit_conversion(frozenset(["millilitre", "litre"]))
        self.assertIsInstance(singleton_unit_conversion, UnitConversion)
        self.assertIs(singleton_unit_conversion, fixture_unit_conversion)