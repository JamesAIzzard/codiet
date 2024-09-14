from unittest import TestCase

from codiet.db_population.units import read_units_from_json, read_global_unit_conversions_from_json
from codiet.utils.map import Map
from codiet.model.units.unit import Unit
from codiet.model.units.ingredient_unit_conversion import IngredientUnitConversion
from codiet.model.ingredients.ingredient import Ingredient

class TestIngredientUnitConversion(TestCase):

    def setUp(self) -> None:
        # Import the global units
        self.global_units = read_units_from_json()
        self.global_unit_conversions = read_global_unit_conversions_from_json()
        # Map them to their names
        self.named_global_units = Map[str, Unit]()
        for global_unit in self.global_units:
            self.named_global_units.add_mapping(global_unit.unit_name, global_unit)

        # Init a test ingredient
        self.ingredient = Ingredient(
            name='test',
            global_units=self.global_units,
            global_unit_conversions=self.global_unit_conversions,
        )

        # Init a test ingredient unit conversion
        self.ingredient_unit_conversion = IngredientUnitConversion(
            ingredient=self.ingredient,
            from_unit=self.named_global_units.get_value('gram'),
            to_unit=self.named_global_units.get_value('millilitre'),
            from_unit_qty=1.0,
            to_unit_qty=1.2
        )

    def test_init(self):
        """Check an ingredient unit conversion can be initialised."""
        # Check everything was set up correctly
        self.assertEqual(self.ingredient_unit_conversion.ingredient, self.ingredient)
        self.assertEqual(self.ingredient_unit_conversion.from_unit, self.named_global_units.get_value('gram'))
        self.assertEqual(self.ingredient_unit_conversion.to_unit, self.named_global_units.get_value('millilitre'))
        self.assertEqual(self.ingredient_unit_conversion.from_unit_qty, 1.0)
        self.assertEqual(self.ingredient_unit_conversion.to_unit_qty, 1.2)

    def test_can_init_with_none_quantities(self):
        """Check an ingredient unit conversion can be initialised with None quantities."""
        # Check everything was set up correctly
        ingredient_unit_conversion = IngredientUnitConversion(
            ingredient=self.ingredient,
            from_unit=self.named_global_units.get_value('gram'),
            to_unit=self.named_global_units.get_value('millilitre'),
        )
        self.assertIsNone(ingredient_unit_conversion.from_unit_qty)
        self.assertIsNone(ingredient_unit_conversion.to_unit_qty)

    def test_from_unit_qty_setter(self):
        """Check the from_unit_qty can be set."""
        # Set the from_unit_qty
        self.ingredient_unit_conversion.from_unit_qty = 2.0
        # Check it was set correctly
        self.assertEqual(self.ingredient_unit_conversion.from_unit_qty, 2.0)

    def test_to_unit_qty_setter(self):
        """Check the to_unit_qty can be set."""
        # Set the to_unit_qty
        self.ingredient_unit_conversion.to_unit_qty = 2.4
        # Check it was set correctly
        self.assertEqual(self.ingredient_unit_conversion.to_unit_qty, 2.4)

    def test_equality(self):
        """Check two ingredient unit conversions are equal if they have the same attributes."""
        # Check if two ingredient unit conversions are equal
        # Create another like the one from setup
        ingredient_unit_conversion = IngredientUnitConversion(
            ingredient=self.ingredient,
            from_unit=self.named_global_units.get_value('gram'),
            to_unit=self.named_global_units.get_value('millilitre'),
            from_unit_qty=1.0,
            to_unit_qty=1.2
        )
        # Check both are considered equal
        self.assertEqual(self.ingredient_unit_conversion, ingredient_unit_conversion)

        # Check they are different if they have different ingredients
        # Create a new different ingredient
        ingredient2 = Ingredient(
            name='test2',
            global_units=self.global_units,
            global_unit_conversions=self.global_unit_conversions,
        )
        ingredient_unit_conversion = IngredientUnitConversion(
            ingredient=ingredient2,
            from_unit=self.named_global_units.get_value('gram'),
            to_unit=self.named_global_units.get_value('millilitre'),
            from_unit_qty=1.0,
            to_unit_qty=1.2
        )
        self.assertNotEqual(self.ingredient_unit_conversion, ingredient_unit_conversion)