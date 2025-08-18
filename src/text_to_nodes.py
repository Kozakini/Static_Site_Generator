from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.Plain_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.Plain_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes



def extract_markdown_images(text):
    img_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    link_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return img_matches, link_matches



def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_images(node.text)[0]
        if links == []:
            new_nodes.append(node)
        else:
            alt_text, link = links.pop(0)
            section = node.text.split(f"![{alt_text}]({link})", 1)
            new_nodes.append(TextNode(section[0], TextType.Plain_text))
            new_nodes.append(TextNode(alt_text, TextType.Images, link))
            while links != []:
                alt_text, link = links.pop(0)
                section = section[1].split(f"![{alt_text}]({link})", 1)
                if section[0] != "":
                    new_nodes.append(TextNode(section[0], TextType.Plain_text))
                new_nodes.append(TextNode(alt_text, TextType.Images, link))
            if len(section) > 1 and section[1] != "":
                new_nodes.append(TextNode(section[1], TextType.Plain_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_images(node.text)[1]
        if links == []:
            new_nodes.append(node)
        else:
            link_text, link = links.pop(0)
            section = node.text.split(f"[{link_text}]({link})", 1)
            new_nodes.append(TextNode(section[0], TextType.Plain_text))
            new_nodes.append(TextNode(link_text, TextType.Links, link))
            while links != []:
                link_text, link = links.pop(0)
                section = section[1].split(f"[{link_text}]({link})", 1)
                if section[0] != "":
                    new_nodes.append(TextNode(section[0], TextType.Plain_text))
                new_nodes.append(TextNode(link_text, TextType.Links, link))
            if len(section) > 1 and section[1] != "":
                new_nodes.append(TextNode(section[1], TextType.Plain_text))

    return new_nodes


def text_to_nodes(text):
    new_node = [TextNode(text, TextType.Plain_text)]
    new_node = split_nodes_delimiter(new_node, "**", TextType.Bold)
    new_node = split_nodes_delimiter(new_node, "_", TextType.Italic)
    new_node = split_nodes_delimiter(new_node, "`", TextType.Code)
    new_node = split_nodes_link(new_node)
    new_node = split_nodes_image(new_node)
    return new_node


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for i  in range(len(blocks)):
        blocks[i] = blocks[i].strip()
        if blocks[i] == "":
            del blocks[i]


    return blocks
