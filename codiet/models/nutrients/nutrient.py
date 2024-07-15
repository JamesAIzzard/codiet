class Nutrient:
    """Class to represent a nutrient."""

    def __init__(
        self,
        id: int,
        nutrient_name: str,
        aliases: list[str] | None = None,
        parent_id: int | None = None,
        child_ids: list[int] | None = None,
    ):
        self.id = id
        self.nutrient_name = nutrient_name
        self.aliases = aliases if aliases is not None else []
        self.parent_id = parent_id
        self.child_ids = child_ids if child_ids is not None else []

    @property
    def is_parent(self) -> bool:
        """Returns True if the nutrient is a parent."""
        return len(self.child_ids) > 0
    
    @property
    def is_child(self) -> bool:
        """Returns True if the nutrient is a child."""
        return self.parent_id is not None