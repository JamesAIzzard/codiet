from codiet.db.stored_entity import StoredEntity

class StoredRefEntity(StoredEntity):
    """Models a stored object which references another object.
    For example, this would be used for an ingredient flag, where
    the flag references an ingredient.
    """

    def __init__(
            self, primary_entity_id:int|None= None, 
            ref_entity_id:int|None=None, 
            *args, **kwargs
        ):
        """Initialise the stored reference object."""
        super().__init__(*args, **kwargs)
        self._ref_entity_id = ref_entity_id
        self._primary_entity_id = primary_entity_id

    @property
    def ref_entity_id(self) -> int | None:
        """Get the reference entity's ID."""
        return self._ref_entity_id

    @ref_entity_id.setter
    def ref_entity_id(self, ref_id: int|None):
        """Set the reference entity's ID."""
        self._ref_entity_id = ref_id

    @property
    def primary_entity_id(self) -> int | None:
        """Get the primary entity's ID."""
        return self._primary_entity_id
    
    @primary_entity_id.setter
    def primary_entity_id(self, primary_entity_id: int|None):
        """Set the primary entity's ID."""
        self._primary_entity_id = primary_entity_id