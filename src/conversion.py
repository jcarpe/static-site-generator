import re
from enum import Enum
from textnode import TextNode, TextType
from htmlnode import LeafNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

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
        
def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        extracted_images = extract_markdown_images(node.text)
        
        if not extracted_images:
            new_nodes.append(node)
            continue
        
        current_text = node.text
        
        for alt_text, url in extracted_images:
            image_markdown = f"![{alt_text}]({url})"
            parts = current_text.split(image_markdown, 1)  # Split only once
            
            # Add text before the image (if any)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGES, url))
            
            # Continue with the remaining text
            current_text = parts[1] if len(parts) > 1 else ""
        
        # Add any remaining text after the last image
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes
    
def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        extracted_links = extract_markdown_links(node.text)
        
        if not extracted_links:
            new_nodes.append(node)
            continue
        
        current_text = node.text
        
        for link_text, url in extracted_links:
            link_markdown = f"[{link_text}]({url})"
            parts = current_text.split(link_markdown, 1)  # Split only once
            
            # Add text before the link (if any)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Add the link node
            new_nodes.append(TextNode(link_text, TextType.LINKS, url))
            
            # Continue with the remaining text
            current_text = parts[1] if len(parts) > 1 else ""
        
        # Add any remaining text after the last link
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type is TextType.TEXT or not delimiter in node.text:
            new_nodes.append(node)
            # print("Skipping node:", node)
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

def text_to_text_nodes(text: str):
    original_text_node = TextNode(text, TextType.TEXT)
    text_nodes = [original_text_node]
    text_nodes = split_nodes_images(text_nodes)
    text_nodes = split_nodes_links(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    return text_nodes

def markdown_to_blocks(markdown: str):
    # For simplicity, split by double newlines to get paragraphs
    blocks = [p.strip() for p in markdown.split("\n\n") if p.strip()]
    return blocks

def block_to_block_type(block: str):
    if block.startswith("# "):
        return BlockType.HEADING
    elif block.startswith("## "):
        return BlockType.HEADING
    elif block.startswith("### "):
        return BlockType.HEADING
    elif block.startswith("#### "):
        return BlockType.HEADING
    elif block.startswith("##### "):
        return BlockType.HEADING
    elif block.startswith("###### "):
        return BlockType.HEADING
    elif block.startswith("> "):
        return BlockType.QUOTE
    elif block.startswith("- ") or block.startswith("* ") or re.match(r"^\d+\. ", block):
        if re.match(r"^\d+\. ", block):
            return BlockType.ORDERED_LIST
        else:
            return BlockType.UNORDERED_LIST
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH
