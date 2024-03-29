def create_nutrient_dict(
    ntr_qty_value=None, ntr_qty_unit="g", ing_qty_value=None, ing_qty_unit="g"
):
    """
    Create a nutrient dictionary with default or provided values.
    """
    return {
        "ntr_qty_value": ntr_qty_value,
        "ntr_qty_unit": ntr_qty_unit,
        "ing_qty_value": ing_qty_value,
        "ing_qty_unit": ing_qty_unit,
    }


def nutrient_is_populated(nutrient: dict) -> bool:
    """Returns True if the nutrient has been populated.
    returns false if any of the value fields are None.
    """
    for value in nutrient.values():
        if value is None:
            return False
        if isinstance(value, str) and value.strip() == "" :
            return False
    return True