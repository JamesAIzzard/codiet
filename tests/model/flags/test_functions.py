from unittest import TestCase

import model

class TestFlagStringToFlagName(TestCase):
    def test_correct_name_is_returned(self):
        self.assertEqual(model.flags.flag_string_to_flag_name("Nut Free"), "nut_free")