import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from conversion import text_node_to_html_node

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

if __name__ == "__main__":
    unittest.main()
