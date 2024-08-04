import unittest

from codiet.db_population.units import read_global_units_from_json
from codiet.db_population.units import read_global_unit_conversions_from_json
from codiet.utils.map import Map
from codiet.models.units.unit import Unit
from codiet.models.units.ingredient_unit_conversion import IngredientUnitConversion
from codiet.models.units.ingredient_units_system import IngredientUnitsSystem
from codiet.models.ingredients.ingredient import Ingredient

class TestEntityUnitsSystem(unittest.TestCase):

    def setUp(self):
        # Grab all the global units and conversions
        self.global_units = read_global_units_from_json()
        self.global_unit_conversions = read_global_unit_conversions_from_json()

        # Map the units to their names
        self.named_global_units = Map[str, Unit]()
        for global_unit in self.global_units:
            self.named_global_units.add_mapping(global_unit.unit_name, global_unit)

        # Create a test ingredient
        self.ingredient = Ingredient(
            name="Test Ingredient",
            global_units=self.global_units,
            global_unit_conversions=self.global_unit_conversions,              
        )        

        # Create a system with disconnected graph
        self.disconnected_system = IngredientUnitsSystem(
            ingredient=self.ingredient,
            global_units=self.global_units,
            global_unit_conversions=self.global_unit_conversions,
        )

        # Create a system where the volumes and masses are connected
        # Create a conversion between grams and millilitres
        gram = self.named_global_units.get_value("gram")
        millilitre = self.named_global_units.get_value("millilitre")
        conversion = IngredientUnitConversion(
            ingredient=self.ingredient,
            from_unit=gram,
            to_unit=millilitre,
            from_unit_qty=1,
            to_unit_qty=1.2,
        )
        self.connected_system = IngredientUnitsSystem(
            ingredient=self.ingredient,
            global_units=self.global_units,
            global_unit_conversions=self.global_unit_conversions,
            ingredient_unit_conversions=set([conversion]),
        )

    def test_init(self):
        """Test the initialisation of EntityUnitsSystem."""
        # Check both of the systems are the right type
        self.assertIsInstance(self.disconnected_system, IngredientUnitsSystem)
        self.assertIsInstance(self.connected_system, IngredientUnitsSystem)

    def test_ingredient(self):
        """Test the retrieval of the ingredient."""
        self.assertEqual(self.disconnected_system.ingredient, self.ingredient)

    def test_gram(self):
        """Test the retrieval of the gram unit."""
        self.assertEqual(self.disconnected_system.gram, self.named_global_units.get_value("gram"))

    def test_convert_between_masses(self):
        """Test the conversion between two masses."""
        # Convert 1 gram to 1 milligram
        gram = self.named_global_units.get_value("gram")
        milligram = self.named_global_units.get_value("milligram")
        self.assertEqual(self.connected_system.convert_units(
            from_unit=gram,
            to_unit=milligram,
            quantity=1,
        ), 1000)

    def test_convert_between_volumes(self):
        """Test the conversion between two volumes."""
        # Convert 1 millilitre to 1 litre
        millilitre = self.named_global_units.get_value("millilitre")
        litre = self.named_global_units.get_value("litre")
        self.assertEqual(self.connected_system.convert_units(
            from_unit=millilitre,
            to_unit=litre,
            quantity=1,
        ), 0.001)

    def test_convert_between_mass_and_volume(self):
        """Test the conversion between mass and volume."""
        # Convert 1 gram to 1 millilitre
        gram = self.named_global_units.get_value("gram")
        millilitre = self.named_global_units.get_value("millilitre")
        self.assertEqual(self.connected_system.convert_units(
            from_unit=gram,
            to_unit=millilitre,
            quantity=1,
        ), 1.2)

        # Convert 1 gram to Litres
        litre = self.named_global_units.get_value("litre")
        self.assertEqual(self.connected_system.convert_units(
            from_unit=gram,
            to_unit=litre,
            quantity=1,
        ), 0.0012)

        # Convert 1 Litre to grams
        self.assertEqual(self.connected_system.convert_units(
            from_unit=litre,
            to_unit=gram,
            quantity=1,
        ), 833.3333333333334)

    def test_add_conversion_and_convert(self):
        """Test adding a conversion and converting."""
        # Setup gram-slice conversion
        gram = self.named_global_units.get_value("gram")
        slice_unit = self.named_global_units.get_value("slice")
        slice_conversion = IngredientUnitConversion(
            ingredient=self.ingredient,
            from_unit=gram,
            to_unit=slice_unit,
            from_unit_qty=100,
            to_unit_qty=1,
        )
        self.disconnected_system.update_entity_unit_conversions(set([slice_conversion]))

        # Convert 200 grams to slices
        self.assertEqual(self.disconnected_system.convert_units(
            from_unit=gram,
            to_unit=slice_unit,
            quantity=200,
        ), 2)

        # Convert 2 slices to grams
        self.assertEqual(self.disconnected_system.convert_units(
            from_unit=slice_unit,
            to_unit=gram,
            quantity=2,
        ), 200)

    