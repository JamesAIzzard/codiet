from codiet.model.quantities import IsQuantified


class QuantityCost(IsQuantified):
    def __init__(self, cost: float | None = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._cost = cost

    @property
    def cost(self) -> float:
        if self._cost is None:
            raise TypeError("Cost not set")
        return self._cost

    @cost.setter
    def cost(self, value: float) -> None:
        if value < 0:
            raise ValueError("Cost cannot be negative.")

        self._cost = value
