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
        self.assertEqual(len(tags), self.NUM_TAGS)

    def test_creates_mapping_with_correct_children(self):
        tag_dtos = self.json_repository.read_all_tag_dtos()
        tags = self.tag_factory.create_tags_from_graph(tag_dtos)
        drink = tags["drink"]
        self.assertEqual(len(drink.direct_parents), 0)
        self.assertEqual(len(drink.direct_children), 2)
        self.assertEqual(
            set(drink.direct_children),
            set(["smoothie", "juice"]),
        )

    def test_creates_mapping_with_correct_parents(self):
        tag_dtos = self.json_repository.read_all_tag_dtos()
        tags = self.tag_factory.create_tags_from_graph(tag_dtos)
        smoothie = tags["smoothie"]
        self.assertEqual(len(smoothie.direct_parents), 1)
        self.assertEqual(len(smoothie.direct_children), 0)
        self.assertEqual(
            set(smoothie.direct_parents),
            set(["drink"]),
        )

    def test_creates_mapping_with_correct_parent_and_child_types(self):
        tag_dtos = self.json_repository.read_all_tag_dtos()
        tags = self.tag_factory.create_tags_from_graph(tag_dtos)
        for tag_name, tag in tags.items():
            for parent_name, parent in tag.direct_parents.items():
                self.assertIsInstance(parent_name, str)
                self.assertIsInstance(parent, Tag)
            for child_name, child in tag.direct_children.items():
                self.assertIsInstance(child_name, str)
                self.assertIsInstance(child, Tag)