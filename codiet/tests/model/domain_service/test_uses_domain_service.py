"""Test classes for the UsesDomainService class."""

from codiet.tests.model import BaseModelTest
from codiet.model.ingredients import Ingredient

class BaseUsesDomainServiceTest(BaseModelTest):
    """Base class for testing UsesDomainService."""
    def tearDown(self) -> None:
        """Reset the domain service after each test."""
        Ingredient._setup_run = False
        # Remove the domain service attribute
        
        return super().tearDown()

class TestConstructor(BaseUsesDomainServiceTest):
    def test_runtime_error_if_child_not_setup(self):
        """Check that a runtime error is raised if a child class is instantiated before setup."""
        with self.assertRaises(RuntimeError):
            Ingredient("Apple")

    def test_no_runtime_error_if_child_setup(self):
        """Check that no runtime error is raised if a child class is instantiated after setup."""
        Ingredient.setup(self.domain_service)
        Ingredient("Apple")