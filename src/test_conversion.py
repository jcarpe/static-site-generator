import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from conversion import (
    BlockType,
    block_to_block_type,
    extract_markdown_images, 
    extract_markdown_links, 
    markdown_to_blocks,
    text_node_to_html_node, 
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_text_nodes
)

class TestMarkdownImageExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "Here is an image: ![Alt text](https://example.com/image.png) and another one ![Another alt](https://example.com/another-image.jpg)"
        expected = [
            ("Alt text", "https://example.com/image.png"),
            ("Another alt", "https://example.com/another-image.jpg")
        ]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

class TestMarkdownLinkExtraction(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "Here is a link: [Link text](https://example.com) and another one [Another link](https://example.com/another-page)"
        expected = [
            ("Link text", "https://example.com"),
            ("Another link", "https://example.com/another-page")
        ]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

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

class TestSplitNodeImages(unittest.TestCase):
    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestSplitNodesLinks(unittest.TestCase):
    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINKS, "https://example.org"),
            ],
            new_nodes,
        )

class TestTextToNodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = "This is **bold** text with _italic_ and `code`."
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), 7)
        self.assertEqual(nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(" text with ", TextType.TEXT))
        self.assertEqual(nodes[3], TextNode("italic", TextType.ITALIC))
        self.assertEqual(nodes[4], TextNode(" and ", TextType.TEXT))
        self.assertEqual(nodes[5], TextNode("code", TextType.CODE))
        self.assertEqual(nodes[6], TextNode(".", TextType.TEXT))

    def test_text_to_nodes_with_images_and_links(self):
        text = "**Here** is an ![image](https://example.com/image.png) _and_ a [link](https://example.com)."
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), 8)
        self.assertEqual(nodes[0], TextNode("Here", TextType.BOLD))
        self.assertEqual(nodes[1], TextNode(" is an ", TextType.TEXT))
        self.assertEqual(nodes[2], TextNode("image", TextType.IMAGES, "https://example.com/image.png"))
        self.assertEqual(nodes[3], TextNode(" ", TextType.TEXT))
        self.assertEqual(nodes[4], TextNode("and", TextType.ITALIC))
        self.assertEqual(nodes[5], TextNode(" a ", TextType.TEXT))
        self.assertEqual(nodes[6], TextNode("link", TextType.LINKS, "https://example.com"))
        self.assertEqual(nodes[7], TextNode(".", TextType.TEXT))

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is the first paragraph.

This is the second paragraph with an ![image](https://example.com/image.png).

This is the third paragraph with a [link](https://example.com).
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "This is the first paragraph.")
        self.assertEqual(blocks[1], "This is the second paragraph with an ![image](https://example.com/image.png).")
        self.assertEqual(blocks[2], "This is the third paragraph with a [link](https://example.com).")

    def test_markdown_to_blocks_with_list(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        md = """
This is **bolded** paragraph

``` python
def hello_world():
    print("Hello, world!")
```

> This is a quote

- This is a list
- with items

1. This is an ordered list
2. with items
"""
        blocks = markdown_to_blocks(md)
        block_types = [block_to_block_type(block) for block in blocks]
        
        self.assertEqual(
            block_types,
            [
                BlockType.PARAGRAPH,
                BlockType.CODE,
                BlockType.QUOTE,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
            ],
        )

if __name__ == "__main__":
    unittest.main()
