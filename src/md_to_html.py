from textnode import TextNode, TextType, text_node_to_html
from block_type import block_to_block_type, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_nodes import split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_nodes, markdown_to_blocks
import re

def text_to_children(text):
    text_nodes = text_to_nodes(text.replace("\n"," "))
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html(text_node))
    return children





def markdown_to_html_node(md):

    blocks = markdown_to_blocks(md)

    i=0

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.Header:
            blocks[i] = HTMLNode(tag = "h1")
        elif block_type == BlockType.Code:
            blocks[i] = HTMLNode(tag = "pre")
        elif block_type == BlockType.Quote:
            blocks[i] = HTMLNode(tag = "blockquote")
        elif block_type == BlockType.Ordered_list:
            blocks[i] = HTMLNode(tag = "ol")
        elif block_type == BlockType.Unordered_list:
            blocks[i] = HTMLNode(tag = "ul")
        else:
            blocks[i] = HTMLNode(tag = "p")

        if block_type == BlockType.Code:
            text_node = TextNode(block.strip("```").lstrip("\n"), TextType.Code)

            children = ParentNode("pre", [text_node_to_html(text_node)])
        else:
            children =  ParentNode(blocks[i].tag, text_to_children(block))

        blocks[i].children = children


        i += 1

    childre = []
    for block in blocks:
        childre.append(block.children)
    parent = ParentNode("div", childre)

    return parent
