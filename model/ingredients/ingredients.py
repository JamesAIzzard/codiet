import typing

class Ingredient:
    def __init__(
        self, 
        name:typing.Optional[str]=None,
        cost_per_g: typing.Optional[float]=None,
    ):
        self.name = name
        self.cost_per_g = cost_per_g