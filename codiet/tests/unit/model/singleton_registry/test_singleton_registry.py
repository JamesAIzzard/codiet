from codiet.tests import BaseCodietTest
from codiet.tests.custom_assertions import assertDictValuesIdentical
from codiet.model import SingletonRegistry

class BaseSingletonRegistryTest(BaseCodietTest):
    
    def setUp(self) -> None:
        super().setUp()       

class TestConstructor(BaseSingletonRegistryTest):

    def test_can_init(self):
        singleton_registry = SingletonRegistry()
        self.assertIsInstance(singleton_registry, SingletonRegistry)

class TestUnits(BaseSingletonRegistryTest):
    
    def test_returns_units(self):
        singleton_registry = SingletonRegistry()

        domain_service_units = singleton_registry.units

        units = self.fixture_manager.quantities_fixtures.units

        self.assertTrue(len(domain_service_units) > 0)
        compare_dicts(self, domain_service_units, units)

class TestGram(BaseSingletonRegistryTest):
    
    def test_returns_gram(self):
        singleton_registry = SingletonRegistry()

        domain_service_gram = singleton_registry.gram

        gram = self.fixture_manager.quantities_fixtures.gram
        self.assertIs(domain_service_gram, gram)

class TestGlobalUnitConversions(BaseSingletonRegistryTest):
        
    def test_returns_global_unit_conversions(self):
        singleton_registry = SingletonRegistry()

        domain_service_global_unit_conversions = singleton_registry.global_unit_conversions

        global_unit_conversions = self.fixture_manager.quantities_fixtures.global_unit_conversions

        self.assertTrue(len(domain_service_global_unit_conversions) > 0)
        compare_dicts(self, domain_service_global_unit_conversions, global_unit_conversions)