from typing import TYPE_CHECKING

from codiet.optimisation import Optimiser

if TYPE_CHECKING:
    from codiet.data import DatabaseService

class OptimiserFactory:

    def __init__(self) -> None:
        self._database_service: "DatabaseService"

    def initialise(self, database_service:"DatabaseService") -> "OptimiserFactory":
        self._database_service = database_service

        Optimiser.initialise(
            database_service=self._database_service
        )

        return self

    def create_optimiser(self) -> Optimiser:
        optimiser = Optimiser()
        return optimiser