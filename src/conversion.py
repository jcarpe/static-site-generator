from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINKS:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGES:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("node text type is not a valid TextType")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type is TextType.TEXT or not delimiter in node.text:
            # new_nodes.append(node)
            print("Skipping node:", node)
        else:
            parts = node.text.split(delimiter)
        
            # Check for invalid markdown (odd number of delimiters)
            if len(parts) % 2 == 0:
                raise ValueError(f"Invalid markdown syntax: unmatched {delimiter}")
            
            for i, part in enumerate(parts):
                if part:  # Skip empty parts
                    # Even indices are normal text, odd indices are formatted text
                    current_type = text_type if i % 2 == 1 else TextType.TEXT
                    new_nodes.append(TextNode(part, current_type))
    return new_nodes