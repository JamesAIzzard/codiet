from codiet.tests import BaseCodietTest
from codiet.utils.graphs import build_graph, GraphNode

class GraphsBaseTest(BaseCodietTest):
    def setUp(self) -> None:
        super().setUp()
        self.test_data = {
            "a": {},
            "b": {
                "c": {},
                "d": {
                    "e": {"b": {}},
                },
            },
        }

        self.tag_graph:dict[str, GraphNode] = build_graph(data = self.test_data)

        self.a = self.tag_graph["a"]
        self.b = self.tag_graph["b"]
        self.c = self.tag_graph["c"]
        self.d = self.tag_graph["d"]
        self.e = self.tag_graph["e"]

class TestBuildGraph(GraphsBaseTest):
    
    def test_graph_has_correct_nodes(self):

        self.assertEqual(len(self.tag_graph), 5)
        for node in self.tag_graph.values():
            self.assertIsInstance(node, GraphNode)

    def test_names_are_set_correctly(self):
        self.assertEqual(self.a.name, "a")
        self.assertEqual(self.b.name, "b")
        self.assertEqual(self.c.name, "c")
        self.assertEqual(self.d.name, "d")
        self.assertEqual(self.e.name, "e")

    def test_direct_children_are_set_correctly(self):
        self.assertEqual(len(self.a.direct_children), 0)
        self.assertEqual(len(self.b.direct_children), 2)
        self.assertIn("c", self.b.direct_children)
        self.assertIn("d", self.b.direct_children)
        self.assertEqual(len(self.c.direct_children), 0)
        self.assertEqual(len(self.d.direct_children), 1)
        self.assertIn("e", self.d.direct_children)
        self.assertEqual(len(self.e.direct_children), 1)
        self.assertIn("b", self.e.direct_children)

    def test_direct_parents_are_set_correctly(self):
        self.assertEqual(len(self.a.direct_parents), 0)
        self.assertEqual(len(self.b.direct_parents), 1)
        self.assertIn("e", self.b.direct_parents)
        self.assertEqual(len(self.c.direct_parents), 1)
        self.assertIn("b", self.c.direct_parents)
        self.assertEqual(len(self.d.direct_parents), 1)
        self.assertIn("b", self.d.direct_parents)
        self.assertEqual(len(self.e.direct_parents), 1)
        self.assertIn("d", self.e.direct_parents)

    def test_is_child(self):
        self.assertFalse(self.a.is_child)
        self.assertTrue(self.b.is_child)
        self.assertTrue(self.c.is_child)
        self.assertTrue(self.d.is_child)
        self.assertTrue(self.e.is_child)

    def test_is_parent(self):
        self.assertFalse(self.a.is_parent)
        self.assertTrue(self.b.is_parent)
        self.assertFalse(self.c.is_parent)
        self.assertTrue(self.d.is_parent)
        self.assertTrue(self.e.is_parent)

    def test_is_direct_parent_of(self):
        self.assertFalse(self.a.is_direct_parent_of("b"))
        self.assertFalse(self.b.is_direct_parent_of("e"))
        self.assertTrue(self.b.is_direct_parent_of("c"))
        self.assertTrue(self.b.is_direct_parent_of("d"))
        self.assertFalse(self.c.is_direct_parent_of("b"))
        self.assertFalse(self.d.is_direct_parent_of("b"))
        self.assertTrue(self.d.is_direct_parent_of("e"))
        self.assertTrue(self.e.is_direct_parent_of("b"))
        self.assertFalse(self.e.is_direct_parent_of("d"))

    def test_is_direct_child_of(self):
        self.assertFalse(self.a.is_direct_child_of("b"))
        self.assertFalse(self.b.is_direct_child_of("c"))
        self.assertFalse(self.b.is_direct_child_of("d"))
        self.assertTrue(self.b.is_direct_child_of("e"))
        self.assertTrue(self.c.is_direct_child_of("b"))
        self.assertTrue(self.d.is_direct_child_of("b"))
        self.assertFalse(self.d.is_direct_child_of("e"))
        self.assertTrue(self.e.is_direct_child_of("d"))

    def test_is_child_of(self):
        self.assertFalse(self.b.is_child_of("a"))
        self.assertTrue(self.e.is_child_of("b"))
        self.assertTrue(self.c.is_child_of("b"))
        self.assertTrue(self.d.is_child_of("b"))
        self.assertTrue(self.b.is_child_of("e"))
        self.assertFalse(self.b.is_child_of("c"))

    def test_is_parent_of(self):
        self.assertFalse(self.a.is_parent_of("b"))
        self.assertTrue(self.b.is_parent_of("e"))
        self.assertTrue(self.b.is_parent_of("c"))
        self.assertTrue(self.b.is_parent_of("d"))
        self.assertTrue(self.b.is_parent_of("b"))
        self.assertTrue(self.e.is_parent_of("b"))
        self.assertFalse(self.c.is_parent_of("b"))
        self.assertTrue(self.d.is_parent_of("b"))
