from typing import TYPE_CHECKING

from codiet.db.stored_entity import StoredEntity
from codiet.models.nutrients.nutrient import Nutrient
from codiet.models.units.unit import Unit

if TYPE_CHECKING:
    from codiet.models.ingredients.ingredient import Ingredient

class IngredientNutrientQuantity(StoredEntity):
    """Class to represent the nutrient quantity associated with an entity."""

    def __init__(
        self,
        nutrient: Nutrient,
        ingredient: 'Ingredient',
        ntr_mass_unit: Unit | None = None,
        ntr_mass_value: float | None = None,
        entity_grams_qty: float | None = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        
        self._nutrient = nutrient
        self._ingredient = ingredient
        self._ntr_mass_unit = ntr_mass_unit
        self._ntr_mass_value = ntr_mass_value
        self._entity_grams_qty = entity_grams_qty

    @property
    def nutrient(self) -> Nutrient:
        """Return the nutrient."""
        return self._nutrient

    @property
    def ingredient(self) -> 'Ingredient':
        """Return the ingredient."""
        return self._ingredient

    @property
    def ntr_mass_unit(self) -> Unit | None:
        """Return the nutrient mass unit."""
        return self._ntr_mass_unit

    @ntr_mass_unit.setter
    def ntr_mass_unit(self, value: Unit):
        """Set the nutrient mass unit."""
        self._ntr_mass_unit = value

    @property
    def ntr_mass_value(self) -> float | None:
        """Return the nutrient mass value."""
        return self._ntr_mass_value

    @ntr_mass_value.setter
    def ntr_mass_value(self, value: float | None):
        """Set the nutrient mass value."""
        self._ntr_mass_value = value

    @property
    def entity_grams_qty(self) -> float | None:
        """Return the entity grams quantity."""
        return self._entity_grams_qty

    @entity_grams_qty.setter
    def entity_grams_qty(self, value: float | None):
        """Set the entity grams quantity."""
        self._entity_grams_qty = value

    def __hash__(self):
        return hash(
            (
                self.ref_entity_id,
                self.primary_entity_id,
                self.id,
                self.nutrient.nutrient_name,
            )
        )

    def __eq__(self, other):
        if not isinstance(other, IngredientNutrientQuantity):
            return False

        attributes_to_compare = [
            ("ref_entity_id", self.ref_entity_id, other.ref_entity_id),
            ("primary_entity_id", self.primary_entity_id, other.primary_entity_id),
            ("id", self.id, other.id),
            (
                "nutrient_name",
                self.nutrient.nutrient_name,
                other.nutrient.nutrient_name,
            ),
        ]

        for attr_name, self_value, other_value in attributes_to_compare:
            if self_value != other_value:
                raise ValueError(
                    f"Mismatch in {attr_name}: {self_value} != {other_value}"
                )

        return True

    def __str__(self):
        return f"{self.nutrient.nutrient_name} quantity"
