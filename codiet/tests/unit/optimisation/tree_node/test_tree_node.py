from codiet.tests import BaseCodietTest
from codiet.optimisation import TreeNode

class BaseTreeNodeTest(BaseCodietTest):
    pass

class TestConstructor(BaseTreeNodeTest):
        
        def test_can_create_tree_node(self):
            tree_node = TreeNode()
    
            self.assertIsInstance(tree_node, TreeNode)

        def test_can_define_with_dict(self):
            tree_node = TreeNode({
                 "day_1": {
                    "breakfast": {
                        "drink": {},
                        "main": {}
                    },
                    "lunch": {
                        "drink": {},
                        "main": {}
                    }
                 },
                    "day_2": {
                        "breakfast": {
                            "drink": {},
                            "main": {}
                        }
                    }
            })

            self.assertIsInstance(tree_node, TreeNode)

class TestGetItem(BaseTreeNodeTest):
    
    def test_can_get_item(self):
        tree_node = TreeNode({
             "breakfast": {
                "drink": {},
                "main": {}
            }
        })

        self.assertIsInstance(tree_node["breakfast"], TreeNode)
        self.assertIsInstance(tree_node["breakfast"]["drink"], TreeNode)
        self.assertIsInstance(tree_node["breakfast"]["main"], TreeNode)