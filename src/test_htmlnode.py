import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node

class TestHTMLNodeConversion(unittest.TestCase):
    def test_text_node_to_html_node(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Hello, world!")

        bold_node = TextNode("Bold text", TextType.BOLD)
        html_node_bold = text_node_to_html_node(bold_node)
        self.assertIsInstance(html_node_bold, LeafNode)
        self.assertEqual(html_node_bold.value, "Bold text")

        italic_node = TextNode("Italic text", TextType.ITALIC)
        html_node_italic = text_node_to_html_node(italic_node)
        self.assertIsInstance(html_node_italic, LeafNode)
        self.assertEqual(html_node_italic.value, "Italic text")

        code_node = TextNode("Code text", TextType.CODE)
        html_node_code = text_node_to_html_node(code_node)
        self.assertIsInstance(html_node_code, LeafNode)
        self.assertEqual(html_node_code.value, "Code text")

        link_node = TextNode("Link text", TextType.LINKS, "https://example.com")
        html_node_link = text_node_to_html_node(link_node)
        self.assertIsInstance(html_node_link, LeafNode)
        self.assertEqual(html_node_link.props, {"href": "https://example.com"})
        self.assertEqual(html_node_link.value, "Link text")

        image_node = TextNode("Image alt text", TextType.IMAGES, "https://example.com/image.png")
        html_node_image = text_node_to_html_node(image_node)
        self.assertIsInstance(html_node_image, LeafNode)
        self.assertEqual(html_node_image.props, {"src": "https://example.com/image.png", "alt": "Image alt text"})
        self.assertEqual(html_node_image.value, "")

        text_node_wrong = TextNode("Hello, world!", "wrong")
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node_wrong)

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "same")
        node2 = HTMLNode("div", "same")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("div", "bleh")
        node2 = HTMLNode("span", "guh")
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("div", "nope", [], {"class": "container", "id": "main"})
        props_html = node.props_to_html()
        self.assertIn('class="container"', props_html)
        self.assertIn('id="main"', props_html)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("p", "Hello, world!", {"class": "text"})
        self.assertEqual(node2.to_html(), '<p class="text">Hello, world!</p>')

class TestParentNode(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()
