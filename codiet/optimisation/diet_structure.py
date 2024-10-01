from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.optimisation.constraints import Constraint
    from codiet.optimisation.goals import Goal
    from codiet.model.recipes import RecipeQuantity

class Node:
    def __init__(self):
        self.constraints = []
        self.goals = []
        self.solutions = {}
        self.children = {}

    def is_leaf(self):
        return not self.children

class DietStructure:
    def __init__(self, structure: dict[str, dict] | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = Node()
        if structure:
            self._build_tree(self.root, structure)

    def _build_tree(self, node: Node, structure_dict: dict):
        for key, sub_dict in structure_dict.items():
            child_node = Node()
            node.children[key] = child_node
            if isinstance(sub_dict, dict):
                self._build_tree(child_node, sub_dict)

    def __call__(self, path: list[str]):
        node = self.root
        for key in path:
            node = node.children[key]
        return node

    def add_constraint(self, constraint: 'Constraint', path: list[str]):
        node = self(path)
        node.constraints.append(constraint)

    def add_goal(self, goal: 'Goal', path: list[str]):
        node = self(path)
        node.goals.append(goal)

    def add_solution(self, solution:'RecipeQuantity', solution_set_id:int, path: list[str]):
        node = self(path)

        if not node.is_leaf():
            raise ValueError("Cannot add solution to a non-leaf node")

        node.solutions[solution_set_id] = solution