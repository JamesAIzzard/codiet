from codiet.model.quantities import Unit

def create_test_units() -> dict[str, Unit]:
    return {
        "gram": Unit(
            name="gram",
            singular_abbreviation="g",
            plural_abbreviation="g",
            type="mass",
        ),
        "kilogram": Unit(
            name="kilogram",
            singular_abbreviation="kg",
            plural_abbreviation="kg",
            aliases=["kgs"],
            type="mass",
        ),
        "millilitre": Unit(
            name="millilitre",
            singular_abbreviation="ml",
            plural_abbreviation="ml",
            type="volume",
        ),
        "litre": Unit(
            name="litre",
            singular_abbreviation="l",
            plural_abbreviation="l",
            type="volume",
        ),
        "cup": Unit(
            name="cup",
            singular_abbreviation="cup",
            plural_abbreviation="cups",
            type="volume",
        ),
        "tablespoon": Unit(
            name="tablespoon",
            singular_abbreviation="tbsp",
            plural_abbreviation="tbsp",
            type="volume",
        ),
        "whole": Unit(
            name="whole",
            singular_abbreviation="whole",
            plural_abbreviation="whole",
            type="grouping",
        ),
    }