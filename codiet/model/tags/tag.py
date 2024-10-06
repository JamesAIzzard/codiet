from typing import TypedDict

class TagDTO(TypedDict):
    name: str

class Tag:
    """Models a tag."""
    
    def __init__(self, name: str, *args, **kwargs):
        """Initialise the tag."""
        super().__init__(*args, **kwargs)
        self._name = name

    @property
    def name(self) -> str:
        """Get the name of the tag."""
        return self._name