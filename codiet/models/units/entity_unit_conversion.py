from codiet.db.stored_ref_entity import StoredRefEntity
from codiet.models.units.unit_conversion import UnitConversion

class EntityUnitConversion(UnitConversion, StoredRefEntity):
    """Models the conversion between two units specifically associated with an entity."""

    def __init__(
        self, *args, **kwargs
    ):
        """Initialises the EntityUnitConversion object.
        Extends the UnitConversion object with an entity_id.
        """
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"EntityUnitConversion(from_unit={self.from_unit}, to_unit={self.to_unit}, ref_entity_id={self.ref_entity_id})"
