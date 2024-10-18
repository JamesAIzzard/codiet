from typing import Mapping, Any, TypedDict, Type, TypeVar
from collections import defaultdict

from codiet.utils.unique_dict import UniqueDict as UD
from codiet.utils.unique_dict import FrozenUniqueDict as FUD

T = TypeVar("T", bound="GraphNode")

class GraphNodeDTO(TypedDict):
    name: str
    direct_parents: list[str]
    direct_children: list[str]

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

def build_dto_dict(data: dict[str, Any]) -> dict[str, GraphNodeDTO]:
    dto_dict: dict[str, GraphNodeDTO] = defaultdict(lambda: GraphNodeDTO(name="", direct_parents=[], direct_children=[]))

    def process_node(name: str, node_data: dict[str, Any], parent: str|None = None):
        dto_dict[name]["name"] = name
        if parent and parent not in dto_dict[name]["direct_parents"]:
            dto_dict[name]["direct_parents"].append(parent)

        for child_name, child_data in node_data.items():
            if child_name not in dto_dict[name]["direct_children"]:
                dto_dict[name]["direct_children"].append(child_name)
            process_node(child_name, child_data, name)

    # Process the top-level nodes
    for name, node_data in data.items():
        process_node(name, node_data)

    return dict(dto_dict)  # Convert defaultdict back to regular dict

def build_graph(data: Mapping[str, GraphNodeDTO],  node_class:Type[T]) -> dict[str, T]:
    nodes: dict[str, T] = {}

    # Phase 1: Create all nodes
    for name, node_dto in data.items():
        nodes[name] = node_class(name=name, parents={}, children={})

    # Phase 2: Set up all relationships
    for name, node_dto in data.items():
        current_node = nodes[name]
        
        # Set up parent relationships
        for parent_name in node_dto['direct_parents']:
            if parent_name in nodes:
                current_node._direct_parents[parent_name] = nodes[parent_name]
                nodes[parent_name]._direct_children[name] = current_node

        # Set up child relationships
        for child_name in node_dto['direct_children']:
            if child_name in nodes:
                current_node._direct_children[child_name] = nodes[child_name]
                nodes[child_name]._direct_parents[name] = current_node

    return nodes