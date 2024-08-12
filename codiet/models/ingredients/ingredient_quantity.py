from typing import TYPE_CHECKING

from codiet.db.stored_entity import StoredEntity

if TYPE_CHECKING:
    from codiet.models.ingredients.ingredient import Ingredient
    from codiet.models.recipes.recipe import Recipe
    from codiet.models.units.unit import Unit

class IngredientQuantity(StoredEntity):
    """Class to represent an ingredient quantity."""

    def __init__(
        self,
        ingredient: 'Ingredient',
        recipe: 'Recipe',
        qty_value: float | None = None,
        qty_unit: 'Unit|None' = None,
        qty_utol: float | None = None,
        qty_ltol: float | None = None,
        *args, **kwargs
    ):
        """Initialises the class."""
        super().__init__(*args, **kwargs)

        self._recipe = recipe
        self._ingredient = ingredient
        self._qty_value = qty_value

        # If the quantity unit is not set, use the ingredient's standard unit
        if qty_unit is None:
            self._qty_unit = self._ingredient.standard_unit
        else:
            # Check the quantity unit is accessible
            if qty_unit not in self._ingredient.unit_system.available_units:
                raise ValueError(f"{qty_unit.unit_name} is not accessible in the unit system.")
            self._qty_unit = qty_unit

        self._upper_tol = qty_utol
        self._lower_tol = qty_ltol

    @property
    def ingredient(self) -> 'Ingredient':
        """Get the ingredient."""
        return self._ingredient
    
    @property
    def recipe(self) -> 'Recipe':
        """Get the recipe."""
        return self._recipe
    
    @property
    def qty_value(self) -> float|None:
        """Get the quantity value."""
        return self._qty_value
    
    @qty_value.setter
    def qty_value(self, qty_value: float|None):
        """Set the quantity value."""
        self._qty_value = qty_value

    @property
    def qty_unit(self) -> 'Unit':
        """Get the quantity unit."""
        return self._qty_unit # type: ignore # checked in __init__
    
    @qty_unit.setter
    def qty_unit(self, qty_unit: 'Unit'):
        """Set the quantity unit."""
        # Check the quantity unit is accessible
        if qty_unit not in self._ingredient.unit_system.available_units:
            raise ValueError(f"{qty_unit.unit_name} is not accessible in the unit system.")
        self._qty_unit = qty_unit

    @property
    def qty_utol(self) -> float|None:
        """Get the upper tolerance."""
        return self._upper_tol
    
    @qty_utol.setter
    def qty_utol(self, qty_utol: float|None):
        """Set the upper tolerance."""
        self._upper_tol = qty_utol

    @property
    def qty_ltol(self) -> float|None:
        """Get the lower tolerance."""
        return self._lower_tol
    
    @qty_ltol.setter
    def qty_ltol(self, qty_ltol: float|None):
        """Set the lower tolerance."""
        self._lower_tol = qty_ltol

    def __eq__(self, other):
        if not isinstance(other, IngredientQuantity):
            return False
        return (self.recipe, self.ingredient) == (other.recipe, other.ingredient)

    def __hash__(self):
        return hash((self.recipe, self.ingredient))        
