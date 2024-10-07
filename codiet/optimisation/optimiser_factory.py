from typing import TYPE_CHECKING

from codiet.optimisation import Optimiser

if TYPE_CHECKING:
    from codiet.model.recipes import RecipeFactory

class OptimiserFactory:
    
    def __init__(self) -> None:
        self._recipe_factory: "RecipeFactory"

    def create_optimiser(self) -> Optimiser:
        optimiser = Optimiser()
        optimiser._recipe_factory = self._recipe_factory
        return optimiser