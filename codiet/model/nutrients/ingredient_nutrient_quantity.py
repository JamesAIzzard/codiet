"""Models a nutrient quantity associated with an ingredient."""

from typing import TYPE_CHECKING

from codiet.db.stored_entity import StoredEntity
from codiet.model.nutrients.nutrient import Nutrient
from codiet.model.units.unit import Unit

if TYPE_CHECKING:
    from codiet.model.ingredients.ingredient import Ingredient

class IngredientNutrientQuantity(StoredEntity):
    """Class to represent the nutrient quantity associated with an entity."""

    def __init__(
        self,
        nutrient: Nutrient,
        ingredient: 'Ingredient',
        nutrient_mass_unit: Unit | None = None,
        nutrient_mass_value: float | None = None,
        ingredient_grams_value: float | None = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        
        self._nutrient = nutrient
        self._ingredient = ingredient
        self._nutrient_mass_unit = nutrient_mass_unit
        self._nutrient_mass_value = nutrient_mass_value
        self._ingredient_grams_value = ingredient_grams_value

    @property
    def nutrient(self) -> Nutrient:
        """Return the nutrient."""
        return self._nutrient

    @property
    def ingredient(self) -> 'Ingredient':
        """Return the ingredient."""
        return self._ingredient

    @property
    def nutrient_mass_unit(self) -> Unit | None:
        """Return the nutrient mass unit."""
        return self._nutrient_mass_unit

    @nutrient_mass_unit.setter
    def nutrient_mass_unit(self, value: Unit):
        """Set the nutrient mass unit."""
        # Check the mass unit is accessible
        if value not in self.ingredient.unit_system.available_units:
            raise ValueError(f"{value.name} is not accessible in the unit system.")
        self._nutrient_mass_unit = value

    @property
    def nutrient_mass_value(self) -> float | None:
        """Return the nutrient mass value."""
        return self._nutrient_mass_value

    @nutrient_mass_value.setter
    def nutrient_mass_value(self, value: float | None):
        """Set the nutrient mass value."""
        self._nutrient_mass_value = value

    @property
    def ingredient_grams_qty(self) -> float | None:
        """Return the entity grams quantity."""
        return self._ingredient_grams_value

    @ingredient_grams_qty.setter
    def ingredient_grams_qty(self, value: float | None):
        """Set the entity grams quantity."""
        self._ingredient_grams_value = value

    def __hash__(self):
        return hash(
            (
                self.ingredient.name,
                self.ingredient.id,
                self.nutrient.nutrient_name,
                self.nutrient.id,
            )
        )

    def __eq__(self, other):
        if not isinstance(other, IngredientNutrientQuantity):
            return False

        if self.ingredient.id != other.ingredient.id:
            return False
        if self.nutrient.id != other.nutrient.id:
            return False
        if self.nutrient.nutrient_name != other.nutrient.nutrient_name:
            return False
        if self.ingredient.name != other.ingredient.name:
            return False

        return True

    def __str__(self):
        return f"{self.nutrient.nutrient_name} quantity"
