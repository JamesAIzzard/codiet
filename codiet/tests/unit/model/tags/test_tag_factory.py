from codiet.tests import BaseCodietTest
from codiet.model.tags import Tag

class BaseTagFactoryTest(BaseCodietTest):
    def setUp(self):
        super().setUp()

class TestCreateTagsFromGraph(BaseTagFactoryTest):
    def test_creates_mapping_of_correct_types(self):
        tag_dtos = self.json_repository.read_all_tag_dtos()
        tags = self.tag_factory.create_tags_from_graph(tag_dtos)
        for tag_name, tag in tags.items():
            self.assertIsInstance(tag_name, str)
            self.assertIsInstance(tag, Tag)

    def test_creates_mapping_of_correct_length(self):
        tag_dtos = self.json_repository.read_all_tag_dtos()
        tags = self.tag_factory.create_tags_from_graph(tag_dtos)
        self.assertEqual(len(tags), 57)

    def test_creates_mapping_with_correct_parents_and_children(self):
        tag_dtos = self.json_repository.read_all_tag_dtos()
        tags = self.tag_factory.create_tags_from_graph(tag_dtos)
        fruit_drink = tags["fruit_drink"]
        self.assertEqual(len(fruit_drink.direct_parents), 1)
        self.assertIn("drink", fruit_drink.direct_parents)
        self.assertEqual(len(fruit_drink.direct_children), 4)
        self.assertEqual(
            set(fruit_drink.direct_children),
            set(["smoothie", "juice", "lemonade", "fruit_punch"]),
        )

    def test_creates_mapping_with_correct_parent_and_child_types(self):
        tag_dtos = self.json_repository.read_all_tag_dtos()
        tags = self.tag_factory.create_tags_from_graph(tag_dtos)
        fruit_drink = tags["fruit_drink"]
        for parent in fruit_drink.direct_parents.values():
            self.assertIsInstance(parent, Tag)
        for child in fruit_drink.direct_children.values():
            self.assertIsInstance(child, Tag)