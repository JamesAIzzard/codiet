"""Test fixtures for tests requiring nutrient instances."""

from codiet.models.nutrients.nutrient import Nutrient

def get_test_nutrients() -> dict[str, Nutrient]:

    # Instantiate some test nutrients
    protein = Nutrient(
        nutrient_name="protein"
    )

    carbohydrate = Nutrient(
        nutrient_name="carbohydrate",
        aliases=["carb", "carbs"]
    )

    glucose = Nutrient(
        nutrient_name="glucose"
    )

    valine = Nutrient(
        nutrient_name="valine"
    )

    # Configure parent child relationships
    protein._set_children([valine])
    valine._set_parent(protein)
    carbohydrate._set_children([glucose])
    glucose._set_parent(carbohydrate)

    # Build and return the dict
    return {
        "protein": protein,
        "carbohydrate": carbohydrate,
        "glucose": glucose,
        "valine": valine
    }
