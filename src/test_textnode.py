import unittest

from textnode import TextNode, TextType, text_node_to_html
from block_type import block_to_block_type, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_nodes import split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_nodes, markdown_to_blocks
from md_to_html import markdown_to_html_node

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_split_all(self):
        self.maxDiff = None
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_nodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.Plain_text),
                TextNode("text", TextType.Bold),
                TextNode(" with an ", TextType.Plain_text),
                TextNode("italic", TextType.Italic),
                TextNode(" word and a ", TextType.Plain_text),
                TextNode("code block", TextType.Code),
                TextNode(" and an ", TextType.Plain_text),
                TextNode("obi wan image", TextType.Images, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.Plain_text),
                TextNode("link", TextType.Links, "https://boot.dev"),
            ],
            nodes,
        )

    def test_markdown_to_blocks(self):
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


    def test_block_type(self):
        md = """
# This is a header

This is a paragraph

```
This is a code block
```

> This is a quote

```
This is a code block

1. This is an ordered list
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [block_to_block_type(block) for block in blocks],
            [
                BlockType.Header,
                BlockType.Paragraph,
                BlockType.Code,
                BlockType.Quote,
                BlockType.Paragraph,
                BlockType.Ordered_list,
            ],
        )


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
