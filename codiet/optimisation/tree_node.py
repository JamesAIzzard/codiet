from typing import Generic, TypeVar

T = TypeVar('T', bound='TreeNode')

DictStructure = dict[str, 'DictStructure']

class TreeNode(Generic[T]):
    def __init__(self, structure:DictStructure|None = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._children: dict[str, 'TreeNode'] = {}

        if structure:
            self._build_from_dict(structure)

    def _build_from_dict(self, structure: DictStructure) -> None:
        for key, value in structure.items():
            child = self._create_child(value)
            self.add_child(key, child)

    def _create_child(self, value: DictStructure) -> 'T':
        return self.__class__(value) # type: ignore

    def add_child(self, key: str, child: 'T|None'=None) -> None:
        self._children[key] = child or self._create_child({})

    def get_child(self, key: str) -> T:
        return self._children[key] # type: ignore

    def remove_child(self, key: str) -> None:
        if key in self._children:
            del self._children[key]
        else:
            raise KeyError(f"Child '{key}' not found")

    def __getitem__(self, key: str) -> T:
        return self.get_child(key)

    def __setitem__(self, key: str, value: 'T') -> None:
        self.add_child(key, value)

    def __delitem__(self, key: str) -> None:
        self.remove_child(key)

    def __contains__(self, key: str) -> bool:
        return key in self._children
    
    def __len__(self) -> int:
        return len(self._children)