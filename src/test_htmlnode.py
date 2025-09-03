import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    # def test_eq(self):
    #     node = HTMLNode("div", "same")
    #     node2 = HTMLNode("div", "same")
    #     self.assertEqual(node, node2)

    # def test_not_eq(self):
    #     node = HTMLNode("div", "bleh")
    #     node2 = HTMLNode("span", "guh")
    #     self.assertNotEqual(node, node2)

    # def test_props_to_html(self):
    #     node = HTMLNode("div", "nope", [], {"class": "container", "id": "main"})
    #     props_html = node.props_to_html()
    #     self.assertIn('class="container"', props_html)
    #     self.assertIn('id="main"', props_html)

    # def test_leaf_to_html_p(self):
    #     node = LeafNode("p", "Hello, world!")
    #     self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    #     node2 = LeafNode("p", "Hello, world!", {"class": "text"})
    #     self.assertEqual(node2.to_html(), '<p class="text">Hello, world!</p>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_large_family(self):
        grandchild_node_a = LeafNode("b", "grandchild a")
        grandchild_node_b = LeafNode("b", "grandchild b")
        grandchild_node_c = LeafNode("b", "grandchild c")
        grandchild_node_d = LeafNode("b", "grandchild d")
        child_node_a = ParentNode("span", [grandchild_node_a, grandchild_node_b])
        child_node_b = ParentNode("span", [grandchild_node_c, grandchild_node_d])
        parent_node = ParentNode("div", [child_node_a, child_node_b])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild a</b><b>grandchild b</b></span><span><b>grandchild c</b><b>grandchild d</b></span></div>",
        )
