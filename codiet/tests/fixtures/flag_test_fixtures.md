## Summary
A collection of test fixtures for flag-related testing.

## IngredientFlag Instances
There is not a cached property for IngredientFlag instances, in the same way that there is for flags, because most tests want to create each instance with respect to a specific ingredient. Instead, we have a create_ingredient_flag() method, which accepts the flag name and the ingredient, and builds an ingredientFlag.

It could be argued that the test could just instantiate an IngredientFlag directly, but putting a builder method on the test fixtures class means that the tests are slightly more decoupled from the initialisation of the instances.
