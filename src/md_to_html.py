from textnode import TextNode, TextType, text_node_to_html
from block_type import block_to_block_type, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_nodes import split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_nodes, markdown_to_blocks
import re
import os
import shutil

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.Paragraph:
        return paragraph_to_html_node(block)
    if block_type == BlockType.Header:
        return heading_to_html_node(block)
    if block_type == BlockType.Code:
        return code_to_html_node(block)
    if block_type == BlockType.Ordered_list:
        return olist_to_html_node(block)
    if block_type == BlockType.Unordered_list:
        return ulist_to_html_node(block)
    if block_type == BlockType.Quote:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_nodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.Plain_text)
    child = text_node_to_html(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def extract_title(markdown):
    to_return = False
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.Header:
            if block[1] != "#":
                to_return = True
                headerd = block.lstrip("#").strip()

    if to_return:
        return headerd
    raise Exception("No h1 headers")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md = f.read()
        node = markdown_to_html_node(md)
        title = extract_title(md)
        html = node.to_html()


    with open(template_path, "r") as l:
        template = l.read()



    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    directory = dest_path.split("/")

    dire = []
    for dir in directory:
        dire.append(dir)
        if not os.path.exists("/".join(dire)) and "/".join(dire) != dest_path:
            os.mkdir("/".join(dire))

    if not os.path.exists(dest_path):
        os.system(f"touch {dest_path.strip('.md')}.html")

    with open(f"{dest_path.strip('.md')}.html", "w") as d:
        d.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    entry = os.listdir(dir_path_content)

    for entr in entry:
        path = os.path.join(dir_path_content, entr)
        if os.path.isfile(path):
            generate_page(path, template_path ,os.path.join(dest_dir_path, entr) )
        else:
            generate_pages_recursive(path, template_path, os.path.join(dest_dir_path, entr))
