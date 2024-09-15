from unittest import mock

from codiet.tests.db.database_test_case import DatabaseTestCase
from codiet.model.flags.flag import Flag
from codiet.model.ingredients.ingredient import Ingredient
from codiet.model.flags.ingredient_flag import IngredientFlag

class TestFlagDBService(DatabaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Create a couple of global flags
        self.vegan_flag = Flag(flag_name="Vegan")
        self.halal_flag = Flag(flag_name="Halal")
        self.vegetarian_flag = Flag(flag_name="Vegetarian")
        self.kosher_flag = Flag(flag_name="Kosher")

        # Create a mock ingredient
        self.mock_ingredient = mock.MagicMock(spec=Ingredient)
        self.mock_ingredient.id = 1

    def test_flag_id_name_map(self):
        """Checks the flag ID to name mapping property is working properly."""
        # Get the flag ID to name map
        flag_id_name_map = self.db_service.flags.flag_id_name_map

        # Check there is nothing in the map
        self.assertEqual(len(flag_id_name_map), 0)

        # Create a couple of global flags
        vegan_flag = self.db_service.flags.create_global_flag(self.vegan_flag)
        halal_flag = self.db_service.flags.create_global_flag(self.halal_flag)

        # Check the map is correct
        self.assertEqual(flag_id_name_map.get_value(vegan_flag.id), "Vegan") # type: ignore
        self.assertEqual(flag_id_name_map.get_value(halal_flag.id), "Halal") # type: ignore

    def test_global_flags(self):
        """Checks the global flags property is working properly."""
        # Get the global flags
        global_flags = self.db_service.flags.global_flags

        # Check there are no flags
        self.assertEqual(len(global_flags), 0)

        # Create a couple of global flags
        _ = self.db_service.flags.create_global_flag(self.vegan_flag)
        _ = self.db_service.flags.create_global_flag(self.halal_flag)

        # Check that the flags are in the collection
        self.assertIn(self.vegan_flag, global_flags)
        self.assertIn(self.halal_flag, global_flags)

    def test_create_global_flag(self):
        """Checks the creation of a global flag."""
        # Check there are no flags
        self.assertEqual(len(self.db_service.flags.global_flags), 0)

        # Create the flag
        _ = self.db_service.flags.create_global_flag(self.vegan_flag)

        # Check the flag is now in the collection
        self.assertIn(self.vegan_flag, self.db_service.flags.global_flags)

        # Check we can get the flag
        self.read_vegan_flag = self.db_service.flags.get_flag_by_name("vegan")

        # Check the flag ID was set
        self.assertIsNotNone(self.read_vegan_flag.id)



    def test_create_global_flags(self):
        """Checks the creation of multiple global flags."""
        # Check there are no flags
        self.assertEqual(len(self.db_service.flags.global_flags), 0)

        # Create the flags
        _ = self.db_service.flags.create_global_flags(
            [self.vegan_flag, self.halal_flag]
        )

        # Read the flags
        created_flags = self.db_service.flags.read_all_global_flags()

        # Check the flags were created
        self.assertEqual(len(created_flags), 2)
        self.assertIn(self.vegan_flag, created_flags)
        self.assertIn(self.halal_flag, created_flags)

    def test_create_ingredient_flag(self):
        """Checks the creation of an ingredient flag."""
        # Check there are no flags saved against the ingredient
        self.assertEqual(len(self.db_service.flags.read_ingredient_flags(self.mock_ingredient)), 0)

        # Create the base flag
        vegan_flag = self.db_service.flags.create_global_flag(self.vegan_flag)

        # Create the ingredient flag
        self.ing_vegan_flag = IngredientFlag(
            ingredient=self.mock_ingredient,
            flag=vegan_flag,
            flag_value=True
        )

        # Save the ingredient flag
        _ = self.db_service.flags.create_ingredient_flag(self.ing_vegan_flag)

        # Read the flags
        created_flags = self.db_service.flags.read_ingredient_flags(self.mock_ingredient)

        # Check the flag was created
        self.assertEqual(len(self.db_service.flags.read_ingredient_flags(self.mock_ingredient)), 1)
        self.assertIn(self.ing_vegan_flag, created_flags)

    def test_update_ingredient_flags(self):
        """Check we can update ingredient flags correctly."""
        # Create the base flag
        vegan_flag = self.db_service.flags.create_global_flag(self.vegan_flag)

        # Create the ingredient flag
        self.ing_vegan_flag = IngredientFlag(
            ingredient=self.mock_ingredient,
            flag=vegan_flag
        )

        # Save the ingredient flag
        self.ing_vegan_flag = self.db_service.flags.create_ingredient_flag(self.ing_vegan_flag)

        # Read the ingredient flag back and check it was false
        read_flags = self.db_service.flags.read_ingredient_flags(self.mock_ingredient)
        for flag in read_flags:
            if flag.flag.id == vegan_flag.id:
                self.assertFalse(flag.value)

        # Update the flag
        self.ing_vegan_flag.value = True
        self.db_service.flags.update_ingredient_flag(self.ing_vegan_flag)

        # Check the flag was updated
        read_flags = self.db_service.flags.read_ingredient_flags(self.mock_ingredient)
        for flag in read_flags:
            if flag.flag.id == vegan_flag.id:
                self.assertTrue(flag.value)

    def test_delete_ingredient_flag(self):
        """Check we can delete an ingredient flag."""
        # Create the global flag
        self.vegan_flag = self.db_service.flags.create_global_flag(self.vegan_flag)
        
        # Create the ingredient flag
        ing_vegan_flag = IngredientFlag(
            ingredient=self.mock_ingredient,
            flag=self.vegan_flag
        )

        # Save the ingredient flag
        ing_vegan_flag = self.db_service.flags.create_ingredient_flag(ing_vegan_flag)

        # Check the ingredient flag was saved
        read_flags = self.db_service.flags.read_ingredient_flags(self.mock_ingredient)
        for flag in read_flags:
            if flag.flag.id == self.vegan_flag.id:
                break
        else:
            self.fail("The ingredient flag was not saved.")

        # Delete the flag
        self.db_service.flags.delete_ingredient_flag(ing_vegan_flag)

        # Check the flag was deleted
        read_flags = self.db_service.flags.read_ingredient_flags(self.mock_ingredient)
        for flag in read_flags:
            if flag.flag.id == self.vegan_flag.id:
                self.fail("The ingredient flag was not deleted.")

