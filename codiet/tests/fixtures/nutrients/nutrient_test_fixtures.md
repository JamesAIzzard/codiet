## Summary
A suite of test fixtures to help with testing of nutrient related functionality.

## create_ingredient_nutrient_quantity
We don't create and cache a bunch of IngredientNutrientQuantity instances because in general we require and instance for a particular ingredient. Instead, we provide a create_ingredient_nutrient_quantity method which acts as an interface to create instances from the nutrient name and the ingredient instance. This method uses the Unit instances also on the fixture.