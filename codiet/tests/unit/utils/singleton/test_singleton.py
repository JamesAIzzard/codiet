from codiet.tests import BaseCodietTest
from codiet.utils import SingletonMeta

class SingletonTestClass(metaclass=SingletonMeta):
    pass

class BaseSingletonTest(BaseCodietTest):
    
    def setUp(self) -> None:
        super().setUp()
        

class TestConstructor(BaseSingletonTest):

    def test_can_init(self):
        singleton_test = SingletonTestClass()
        self.assertIsInstance(singleton_test, SingletonTestClass)

    def test_is_singleton(self):
        singleton_test = SingletonTestClass()
        singleton_test_2 = SingletonTestClass()
        self.assertIs(singleton_test, singleton_test_2)

class TestReset(BaseSingletonTest):

    def test_can_reset(self):
        singleton_test = SingletonTestClass()
        singleton_test_2 = SingletonTestClass()

        self.assertIs(singleton_test, singleton_test_2)

        SingletonTestClass.reset()

        singleton_test_3 = SingletonTestClass()
        self.assertIsNot(singleton_test, singleton_test_3)


