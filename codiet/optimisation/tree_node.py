DictStructure = dict[str, 'DictStructure']

class TreeNode:
    def __init__(self, structure:DictStructure|None = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._children: dict[str, 'TreeNode'] = {}

        if structure:
            self._build_from_dict(structure)

    def _build_from_dict(self, structure: dict):
        for key, value in structure.items():
            child = TreeNode(value if isinstance(value, dict) else None)
            self.add_child(key, child)

    def add_child(self, key: str, child: 'TreeNode') -> None:
        self._children[key] = child

    def get_child(self, key: str) -> 'TreeNode':
        return self._children[key]

    def remove_child(self, key: str) -> None:
        if key in self._children:
            del self._children[key]
        else:
            raise KeyError(f"Child '{key}' not found")

    def __getitem__(self, key: str) -> 'TreeNode':
        return self.get_child(key)

    def __setitem__(self, key: str, value: 'TreeNode') -> None:
        self.add_child(key, value)

    def __delitem__(self, key: str) -> None:
        self.remove_child(key)

    def __contains__(self, key: str) -> bool:
        return key in self._children