from .flag import Flag
from codiet.db.stored_ref_entity import StoredRefEntity

class EntityFlag(StoredRefEntity, Flag):
    """Models a flag that is associated with an entity.
    For example, this would be used for an ingredient flag, where
    the flag references an ingredient.
    """

    def __init__(self, flag_id:int|None=None, *args, **kwargs):
        """Initialise the entity flag.
        Args:
            entity_id (int): The ID of the entity that the flag is associated with.
        """
        super().__init__(primary_entity_id=flag_id, *args, **kwargs)

    # Create an alias to redirect the primary entity id to be called flag id