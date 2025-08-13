from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        wordy = ""
        for word in node.text:
            if word != delimiter:
                wordy += word
            if word == delimiter:
                if delimiter not in wordy:
                    new_nodes.append(TextNode(wordy, TextType.Plain_text))
                    wordy = delimiter
                else:
                    new_nodes.append(TextNode(wordy.strip(delimiter), text_type))
                    wordy = ""
    new_nodes.append(TextNode(wordy, TextType.Plain_text))
    return new_nodes

def extract_markdown_images(text):
    img_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    link_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return img_matches, link_matches
