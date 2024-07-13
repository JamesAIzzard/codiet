from codiet.models.units.unit_conversion import UnitConversion

class EntityUnitConversion(UnitConversion):
    """Models the conversion between two units specifically associated with an entity."""

    def __init__(
        self,
        entity_id: int,
        *args, **kwargs
    ):
        """Initialises the EntityUnitConversion object.
        Extends the UnitConversion object with an entity_id.
        Args:
            id (int): The id of the conversion.
            entity_id (int): The id of the entity.
            from_unit_id (int): The id of the unit to convert from.
            to_unit_id (int): The id of the unit to convert to.
            from_unit_qty (float): The quantity of the from unit.
            to_unit_qty (float): The quantity of the to unit.
        """
        super().__init__(*args, **kwargs)
        self.ingredient_id = entity_id
