from typing import Mapping, Any

from codiet.utils.unique_dict import UniqueDict as UD
from codiet.utils.unique_dict import FrozenUniqueDict as FUD

class GraphNode:
    def __init__(
        self,
        name: str,
        parents: Mapping[str, Any],
        children: Mapping[str, Any],
    ):
        self._name: str = name
        self._direct_parents = UD(parents)
        self._direct_children = UD(children)

    @property
    def name(self) -> str:
        return self._name

    @property
    def direct_parents(self) -> FUD[str, Any]:
        return self._direct_parents.immutable

    @property
    def direct_children(self) -> FUD[str, Any]:
        return self._direct_children.immutable

    @property
    def is_child(self) -> bool:
        return len(self._direct_parents) > 0

    @property
    def is_parent(self) -> bool:
        return len(self._direct_children) > 0

    def is_direct_parent_of(self, node_name: str) -> bool:
        return node_name in self._direct_children

    def is_direct_child_of(self, node_name: str) -> bool:
        return node_name in self._direct_parents

    def is_parent_of(self, node_name: str) -> bool:
        visited = set()
        def dfs(current_node):
            if current_node.name == node_name:
                return True
            visited.add(current_node.name)
            for child in current_node.direct_children.values():
                if child.name not in visited and dfs(child):
                    return True
            return False
        return dfs(self)
    
    def is_child_of(self, node_name: str) -> bool:
        visited = set()
        def dfs(current_node):
            if current_node.name == node_name:
                return True
            visited.add(current_node.name)
            for parent in current_node.direct_parents.values():
                if parent.name not in visited and dfs(parent):
                    return True
            return False
        return dfs(self)

def build_graph(data: dict[str, Any]) -> dict[str, Any]:
    nodes: dict[str, GraphNode] = {}

    def create_nodes(name: str, node_data: dict[str, Any]):
        if name not in nodes:
            nodes[name] = GraphNode(name=name, parents={}, children={})
            for child_name, child_data in node_data.items():
                create_nodes(child_name, child_data)

    def set_relationships(name: str, node_data: dict[str, Any]):
        for child_name, child_data in node_data.items():
            nodes[name]._direct_children[child_name] = nodes[child_name]
            nodes[child_name]._direct_parents[name] = nodes[name]
            set_relationships(child_name, child_data)

    # Take a two phase approach to avoid recursion errors.
    for name, node_data in data.items():
        create_nodes(name, node_data)

    for name, node_data in data.items():
        set_relationships(name, node_data)

    return nodes



