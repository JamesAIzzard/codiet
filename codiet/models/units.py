class Unit:
    """A global measurement unit."""

    def __init__(
        self,
        global_unit_id: int,
        unit_name: str,
        plural_name: str,
        type: str,
        conversions: dict[int, float],
    ):
        self.global_unit_id = global_unit_id
        self.unit_name = unit_name
        self.plural_name = plural_name
        self.type = type
        self.convertions = conversions

class IngredientUnit(Unit):
    """An measurement unit associated with an ingredient."""

    def __init__(
        self,
        ingredient_unit_id: int,
        ingredient_id: int,
        ref_unit_id: int,
        custom_unit_qty: float|None,
        ref_unit_qty: float|None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.ingredient_unit_id = ingredient_unit_id
        self.ingredient_id = ingredient_id
        self.ref_unit_id = ref_unit_id
        self.custom_unit_qty = custom_unit_qty
        self.ref_unit_qty = ref_unit_qty
