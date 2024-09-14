from unittest import TestCase

from codiet.utils.map import Map
from codiet.db_population.nutrients import read_global_nutrients_from_json
from codiet.model.nutrients.nutrient import Nutrient

class TestNutrient(TestCase):

    def setUp(self) -> None:
        # Grab all the global nutrients
        self.global_nutrients = read_global_nutrients_from_json()

        # Map them to their names
        self.named_global_nutrients = Map[str, Nutrient]()
        for global_nutrient in self.global_nutrients:
            self.named_global_nutrients.add_mapping(global_nutrient.nutrient_name, global_nutrient)

    def test_init(self):
        """Test the minimal initialisation of Nutrient class."""
        # Create a Nutrient object with 'test' as the nutrient name
        nutrient = Nutrient(
            nutrient_name='test',
            aliases=set(["test_alias", "test_alias2"])
        )

        # Check if the nutrient name is set correctly
        self.assertEqual(nutrient.nutrient_name, 'test')

        # Check if the aliases list is set correctly
        self.assertEqual(nutrient.aliases, frozenset(["test_alias", "test_alias2"]))

        # Check if the parent attribute is None
        self.assertIsNone(nutrient.parent)

        # Check if the children list is empty
        self.assertEqual(nutrient.children, frozenset())

    def test_is_parent(self):
        """Test the is_parent property of Nutrient class."""
        # Fetch protein
        protein = self.named_global_nutrients.get_value('protein')
        # Check protein is a parent
        self.assertTrue(protein.is_parent)


    def test_is_child(self):
        """Test the is_child property of Nutrient class."""
        # Fetch glucose
        glucose = self.named_global_nutrients.get_value('glucose')
        # Check glucose is a child
        self.assertTrue(glucose.is_child)

    def test_is_parent_of(self):
        """Test the is_parent_of method of Nutrient class."""
        # Fetch protein
        protein = self.named_global_nutrients.get_value('protein')
        # Fetch histadine
        histidine = self.named_global_nutrients.get_value('histidine')
        # Check protein is a parent of histadine
        self.assertTrue(protein.is_parent_of(histidine))

    def test_is_child_of(self):
        """Test the is_child_of method of Nutrient class."""
        # Fetch histidine
        histidine = self.named_global_nutrients.get_value('histidine')
        # Fetch protein
        protein = self.named_global_nutrients.get_value('protein')
        # Check histidine is a child of protein
        self.assertTrue(histidine.is_child_of(protein))