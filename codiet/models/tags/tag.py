from codiet.db.stored_entity import StoredEntity

class Tag(StoredEntity):
    """Models a tag."""
    
    def __init__(self, tag_name: str, *args, **kwargs):
        """Initialise the tag."""
        super().__init__(*args, **kwargs)
        self._tag_name = tag_name

    @property
    def tag_name(self) -> str:
        """Get the name of the tag."""
        return self._tag_name