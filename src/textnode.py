from enum import Enum
from htmlnode import LeafNode, HTMLNode, ParentNode

class TextType(Enum):
    Plain_text = "plain_text"
    Bold = "bold"
    Code = "code"
    Links = "link"
    Images = "image"
    Italic = "italic"

class TextNode:
    def __init__(self, text, text_type, link = None):
        self.text = text
        self.text_type = text_type
        self.url = link

    def __eq__(self, other):
        if self.text_type == other.text_type:
            return True

    def __repr__(self):
        return f"TextNode( {self.text}, {self.text_type}, {self.url})"

def text_node_to_html(text_node):
    match text_node.text_type:
        case TextType.Plain_text:
            return LeafNode( None, text_node.text)
        case TextType.Bold:
            return LeafNode("b", text_node.text)
        case TextType.Italic:
            return LeafNode("i", text_node.text)
        case TextType.Code:
            return LeafNode("code", text_node.text)
        case TextType.Links:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.Images:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Unknown text type: {text_node.text_type}")
