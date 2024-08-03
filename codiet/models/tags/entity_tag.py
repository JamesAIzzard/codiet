from codiet.db.stored_ref_entity import StoredRefEntity
from codiet.models.tags.tag import Tag

class EntityTag(StoredRefEntity, Tag):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)