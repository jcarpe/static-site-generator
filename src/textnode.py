from enum import Enum

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        return (
            node.text == self.text and
            node.text_type == self.text_type and
            node.url == self.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
