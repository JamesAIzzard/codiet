from typing import TYPE_CHECKING, Collection

if TYPE_CHECKING:
    from codiet.optimisation.constraints import Constraint
    from codiet.optimisation.goals import Goal
    from codiet.model.recipes import RecipeQuantity

class DietStructureNode:
    def __init__(
        self,
        name: str,
        structure: 'DietStructure',
        parent: 'DietStructureNode|None' = None
    ):
        self.name = name
        self.structure = structure
        self.parent = parent
        self.constraints = []
        self.goals = []
        self.solutions = {}
        self.children = {}

    def is_recipe_node(self):
        return not self.children

    def add_child(self, name: str) -> 'DietStructureNode':
        child_node = DietStructureNode(name, self.structure, parent=self)
        self.children[name] = child_node
        return child_node

    def get_path(self) -> tuple[str, ...]:
        path = []
        node = self
        while node.parent is not None:
            path.insert(0, node.name)
            node = node.parent
        return tuple(path)


class DietStructure:
    def __init__(self, structure: dict[str, dict]|None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = DietStructureNode(name='root', structure=self)
        self.nodes_by_path = {}
        if structure:
            self._build_tree(self.root, structure)

    def _build_tree(self, parent_node: DietStructureNode, structure_dict: dict):
        for key, sub_dict in structure_dict.items():
            child_node = parent_node.add_child(key)
            path = child_node.get_path()
            self.nodes_by_path[tuple(path)] = child_node
            if isinstance(sub_dict, dict) and sub_dict:
                self._build_tree(child_node, sub_dict)

    def __call__(self, path: Collection[str]) -> DietStructureNode:
        if path == []:
            return self.root
        else:
            return self.nodes_by_path.get(tuple(path), None)

    def add_constraint(self, constraint: 'Constraint', path: list[str]):
        node = self(path)
        if node is None:
            raise ValueError(f"No node found at path: {path}")
        node.constraints.append(constraint)

    def add_goal(self, goal: 'Goal', path: list[str]):
        node = self(path)
        if node is None:
            raise ValueError(f"No node found at path: {path}")
        node.goals.append(goal)

    def add_solution(self, solution: 'RecipeQuantity', solution_set_id: int, path: list[str]):
        node = self(path)
        if node is None:
            raise ValueError(f"No node found at path: {path}")
        if not node.is_recipe_node():
            raise ValueError("Cannot add solution to a non-recipe node")
        node.solutions[solution_set_id] = solution

    @property
    def recipe_node_addresses(self) -> list[tuple[str, ...]]:
        addresses = []
        for node in self.nodes_by_path.values():
            if node.is_recipe_node():
                addresses.append(node.get_path())
        return addresses
