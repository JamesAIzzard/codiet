from typing import TYPE_CHECKING, Collection

from codiet.utils.unique_collection import MutableUniqueCollection as MUC
from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC

if TYPE_CHECKING:
    from codiet.optimisation.constraints import Constraint
    from codiet.optimisation.goals import Goal
    from codiet.model.recipes import Recipe


class DietStructureNode:
    def __init__(
        self,
        name: str,
        structure: "DietStructure",
        parent: "DietStructureNode|None" = None,
    ):
        self._name = name
        self._structure = structure
        self._parent = parent
        self._direct_constraints = MUC["Constraint"]()
        self._direct_goals = MUC["Goal"]()
        self._solutions = {}
        self._children = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def direct_constraints(self) -> IUC["Constraint"]:
        return self._direct_constraints.immutable

    @property
    def direct_goals(self) -> MUC["Goal"]:
        return self._direct_goals

    @property
    def solutions(self) -> dict[int, "Recipe"]:
        return self._solutions

    @property
    def address(self) -> tuple[str, ...]:
        path = []
        node = self
        while node._parent is not None:
            path.insert(0, node.name)
            node = node._parent
        return tuple(path)

    @property
    def is_recipe_node(self):
        return not self._children

    @property
    def has_recipe_solutions(self):
        return len(self._solutions) > 0

    def _add_child(self, name: str) -> "DietStructureNode":
        child_node = DietStructureNode(name, self._structure, parent=self)
        self._children[name] = child_node
        return child_node

    def add_constraint(self, constraint: "Constraint") -> "DietStructureNode":
        self._direct_constraints.append(constraint)
        return self

    def add_goal(self, goal: "Goal"):
        self._direct_goals.append(goal)

    def add_solution(self, solution: "Recipe", solution_set_id: int):
        if not self.is_recipe_node:
            raise ValueError("Cannot add solution to a non-recipe node")
        self._solutions[solution_set_id] = solution


class DietStructure:
    def __init__(self, structure: dict[str, dict] | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._root = DietStructureNode(name="root", structure=self)
        self._nodes_by_path = {}
        if structure:
            self._build_tree(self._root, structure)

    def _build_tree(self, parent_node: DietStructureNode, structure_dict: dict):
        for key, sub_dict in structure_dict.items():
            child_node = parent_node._add_child(key)
            path = child_node.address
            self._nodes_by_path[tuple(path)] = child_node
            if isinstance(sub_dict, dict) and sub_dict:
                self._build_tree(child_node, sub_dict)

    def add_constraint(
        self, address: tuple[str, ...], constraint: "Constraint"
    ) -> "DietStructure":
        node = self.get_node(address)
        node.add_constraint(constraint)
        return self

    def get_constraints(self, address: tuple[str, ...]) -> IUC["Constraint"]:
        node = self.get_node(address)
        nodes = []
        # Collect nodes from root to the specified node
        while node is not None:
            nodes.insert(0, node)
            node = node._parent
        constraints = list["Constraint"]()
        # Collect constraints from root to the specified node
        for n in nodes:
            constraints.extend(n._direct_constraints)
        return IUC(constraints)


    def get_node(self, path: tuple[str, ...]) -> DietStructureNode:
        if path == ():
            return self._root
        return self._nodes_by_path[path]

    def get_child_solutions(self, starting_from_node: tuple[str, ...] | None = None) -> list["Recipe"]:
        node = self.get_node(starting_from_node or ())
        recipes = []

        def traverse(n: DietStructureNode):
            if n.has_recipe_solutions:
                recipes.extend(n.solutions.values())
            for child in n._children.values():
                traverse(child)

        traverse(node)
        return recipes


    def solution_node_addresses(
        self, starting_from_node: tuple[str, ...] | None = None
    ) -> list[tuple[str, ...]]:
        node = self.get_node(starting_from_node or ())
        addresses = []

        def traverse(n: DietStructureNode):
            if n.is_recipe_node:
                addresses.append(n.address)
            for child in n._children.values():
                traverse(child)

        traverse(node)
        return addresses


    def solution_nodes(
        self, starting_from_node: tuple[str, ...] | None = None
    ) -> IUC[DietStructureNode]:
        node = self.get_node(starting_from_node or ())
        nodes = []

        def traverse(n: DietStructureNode):
            if n.is_recipe_node:
                nodes.append(n)
            for child in n._children.values():
                traverse(child)

        traverse(node)
        return IUC(nodes)

