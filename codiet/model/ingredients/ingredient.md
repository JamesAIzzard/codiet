## Summary
This is the class responsible for modelling an ingredient in the system.

## Removing `IngredientFlag` and `IngredientNutrientQuantity` instances
Currently, I am doing this by passing the actual `IngredientFlag` or `IngredientNutrientQuantity` instance I want to remove. I was considering writing these removal methods to accept just the name, but the idea of matching against the exact reference is appealing. Currently, I am sticking with removal by instance.