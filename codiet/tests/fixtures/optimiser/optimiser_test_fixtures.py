from codiet.tests.fixtures import BaseTestFixture
from codiet.tests.fixtures.recipes import RecipeTestFixtures
from codiet.optimisation.optimiser import Optimiser
from codiet.optimisation import algorithms

class OptimiserTestFixtures(BaseTestFixture):

    def __init__(self) -> None:
        self._recipe_fixtures = RecipeTestFixtures.get_instance()
        self._deterministic_optimiser:Optimiser|None = None

    @property
    def deterministic_optimiser(self) -> Optimiser:
        if self._deterministic_optimiser is None:
            self._deterministic_optimiser = self.create_deterministic_optimiser()
        return self._deterministic_optimiser
    
    def create_deterministic_optimiser(self) -> Optimiser:
        optimiser = Optimiser()
        optimiser.set_algorithm(algorithms.Deterministic())
        optimiser.set_recipe_source(self._recipe_fixtures.recipes.values())
        return optimiser
