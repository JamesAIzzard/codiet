from typing import TYPE_CHECKING, Mapping

from codiet.utils.unique_dict import FrozenUniqueDict as FUD
from codiet.model.tags.tag import Tag

if TYPE_CHECKING:
    from codiet.model.tags import TagDTO

class TagFactory:

    def create_tags_from_graph(self, tag_graph: Mapping[str, "TagDTO"]) -> FUD[str, Tag]:
        tags: dict[str, Tag] = {}
        
        # First pass: Create all the tags defined in the graph
        for tag_name, tag_dto in tag_graph.items():
            tags[tag_name] = Tag(tag_name, {}, {})
        
        # Second pass: Establish relationships between tags
        for tag_name, tag_dto in tag_graph.items():
            current_tag = tags[tag_name]
            
            # Set parent relationships
            for parent_name in tag_dto.get("direct_parents", []):
                if parent_name in tags:
                    parent_tag = tags[parent_name]
                    current_tag._direct_parents[parent_name] = parent_tag
                    parent_tag._direct_children[tag_name] = current_tag
            
            # Set child relationships
            for child_name in tag_dto.get("direct_children", []):
                if child_name in tags:
                    child_tag = tags[child_name]
                    current_tag._direct_children[child_name] = child_tag
                    child_tag._direct_parents[tag_name] = current_tag

        return FUD(tags)
