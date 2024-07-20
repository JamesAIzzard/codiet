class EntityNutrientQuantity:
    """Class to represent the nutrient quantity associated with an entity.

    Attributes:
        nutrient_id (int): The unique identifier of the associated nutrient.
        ntr_mass_unit_id (int): The unique identifier of the nutrient mass unit.
        ntr_mass_value (float | None, optional): The value of the nutrient mass. Defaults to None.
        entity_grams_value (float | None, optional): The value of the entity in grams. Defaults to None.
        id (int | None): The unique identifier of the nutrient quantity. Defaults to None.
        parent_entity_id (int|None): The unique identifier of the parent entity. Defaults to None.
    """

    def __init__(
        self,
        nutrient_id: int,
        ntr_mass_unit_id: int,
        ntr_mass_value: float | None = None,
        entity_grams_value: float | None = None,
        id: int|None=None,
        entity_id: int|None=None,        
    ):
        self.id = id
        self.nutrient_id = nutrient_id
        self.parent_entity_id = entity_id
        self.nutrient_mass_value = ntr_mass_value
        self.nutrient_mass_unit_id = ntr_mass_unit_id
        self.entity_grams_value = entity_grams_value