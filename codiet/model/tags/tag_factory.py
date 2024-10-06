from typing import TYPE_CHECKING

from codiet.model.tags.tag import Tag

if TYPE_CHECKING:
    from codiet.model.tags import TagDTO

class TagFactory:
    
    def create_tag_from_dto(self, tag_dto: "TagDTO") -> Tag:
        return Tag(tag_dto["name"])