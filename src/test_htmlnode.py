import unittest

from htmlnode import HTMLNode

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
