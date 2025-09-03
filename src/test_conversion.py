import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from conversion import text_node_to_html_node, split_nodes_delimiter

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

class TestNodeSplitting(unittest.TestCase):
    def test_split_nodes_bold_delimiter(self):
        old_nodes = [
            TextNode("Hello, **world**!", TextType.TEXT)
        ]
        delimiter = "**"
        text_type = TextType.BOLD

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "Hello, ")
        self.assertEqual(new_nodes[1].text, "world")
        self.assertEqual(new_nodes[2].text, "!")

        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_italics_delimiter(self):
        old_nodes = [
            TextNode("Hello, _world_!", TextType.TEXT)
        ]
        delimiter = "_"
        text_type = TextType.ITALIC

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "Hello, ")
        self.assertEqual(new_nodes[1].text, "world")
        self.assertEqual(new_nodes[2].text, "!")

        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_code_delimiter(self):
        old_nodes = [
            TextNode("Hello, `world`!", TextType.TEXT)
        ]
        delimiter = "`"
        text_type = TextType.CODE

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "Hello, ")
        self.assertEqual(new_nodes[1].text, "world")
        self.assertEqual(new_nodes[2].text, "!")

        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_multiple_instances(self):
        old_nodes = [
            TextNode("**Hello**, **world**!", TextType.TEXT)
        ]
        delimiter = "**"
        text_type = TextType.BOLD

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(new_nodes[0].text, "Hello")
        self.assertEqual(new_nodes[1].text, ", ")
        self.assertEqual(new_nodes[2].text, "world")
        self.assertEqual(new_nodes[3].text, "!")

        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)

if __name__ == "__main__":
    unittest.main()
