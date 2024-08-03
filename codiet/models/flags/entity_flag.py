from .flag import Flag
from codiet.db.stored_ref_entity import StoredRefEntity

class EntityFlag(Flag, StoredRefEntity):
    """Models a flag that is associated with an entity.
    For example, this would be used for an ingredient flag, where
    the flag references an ingredient.
    """

    def __init__(self, *args, **kwargs):
        """Initialise the entity flag."""
        super().__init__(*args, **kwargs)
