from collections import UserDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.optimisation.problems import DietProblem
    from codiet.optimisation.solutions import DietSolution

class DietStructure(UserDict):
    def __init__(self, name: str, parent: 'DietProblem|DietSolution|None' = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name
        self._parent = parent

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_leaf(self) -> bool:
        return len(self.data) == 0

    @property
    def address(self) -> list[str]:
        address = []
        current = self
        while current is not None:
            address.insert(0, current.name)
            current = current._parent
        return address

    @property
    def leaf_addresses(self) -> list[list[str]]:
        if self.is_leaf:
            return [self.address]
        
        addresses = []
        for subnode in self.data.values():
            addresses.extend(subnode.leaf_addresses)
        return addresses