from typing import Collection

from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.db.stored_entity import StoredEntity

class Nutrient(StoredEntity):
    """Class to represent a nutrient.
    Note:
        Parent and child nutrients are only settable by private methods.
        These operations should never be needed by consumers of the Nutrient class.
        The nutrient tree is constructed at application startup.
    """

    def __init__(
        self,
        nutrient_name: str,
        aliases: Collection[str]|None = None,
        parent: 'Nutrient | None' = None,
        children: Collection['Nutrient'] | None = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._nutrient_name = nutrient_name

        # Check supplied aliases are unique, or init empty list if not supplied
        if aliases is not None:
            if len(aliases) != len(set(aliases)):
                raise ValueError("Aliases must be unique.")
        else:
            aliases = []

        self._aliases = aliases
        self._parent = parent
        self._children = IUC(children) if children is not None else IUC['Nutrient']()

    @property
    def name(self) -> str:
        """Get the name of the nutrient."""
        return self._nutrient_name

    @property
    def aliases(self) -> frozenset[str]:
        """Get the aliases of the nutrient."""
        return frozenset(self._aliases)

    @property
    def parent(self) -> 'Nutrient|None':
        """Get the parent of the nutrient."""
        return self._parent

    @property
    def children(self) -> frozenset['Nutrient']:
        """Get the children of the nutrient."""
        return frozenset(self._children)

    @property
    def is_parent(self) -> bool:
        """Returns True if the nutrient is a parent."""
        return len(self.children) > 0
    
    @property
    def is_child(self) -> bool:
        """Returns True if the nutrient is a child."""
        return self.parent is not None

    def is_parent_of(self, nutrient: 'Nutrient') -> bool:
        """Returns True if the nutrient is a parent of the given nutrient, including children of children."""
        if nutrient in self.children:
            return True
        for child in self.children:
            if child.is_parent_of(nutrient):
                return True
        return False
    
    def is_child_of(self, nutrient: 'Nutrient') -> bool:
        """Returns True if the nutrient is a child of the given nutrient, including parents of parents."""
        if self.parent == nutrient:
            return True
        if self.parent is not None:
            return self.parent.is_child_of(nutrient)
        return False

    def _set_parent(self, parent:'Nutrient') -> None:
        """Sets the instance's parent nutrient."""
        self._parent = parent

    def _set_children(self, children: Collection['Nutrient']) -> None:
        """Add children to the nutrient."""
        self._children = IUC(children)

    def __eq__(self, other):
        if isinstance(other, Nutrient):
            return self.id == other.id and self.name == other.name
        return False

    def __hash__(self):
        return hash((self.id, self.name))