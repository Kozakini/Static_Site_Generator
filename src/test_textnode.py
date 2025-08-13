import unittest

from textnode import TextNode, TextType, text_node_to_html
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_nodes import split_nodes_delimiter, extract_markdown_images
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.Bold)
        node2= TextNode("This is a text node", TextType.Bold)
        self.assertEqual(node, node2)


    def test_props_to_html(self):
        node = HTMLNode("a", "This is a link node", {"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), 'href="https://www.boot.dev"')

    def test_to_html_with_children(self):
            child_node = LeafNode("p", "child")
            parent_node = ParentNode("div", [child_node])
            self.assertEqual(parent_node.to_html(), "<div><p>child</p></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_and_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parenter_node = ParentNode("div", [child_node])
        parent_node = ParentNode("h1", [parenter_node])
        self.assertEqual(
            parent_node.to_html(),
            "<h1><div><span><b>grandchild</b></span></div></h1>",
        )

    def test_to_html_with_link(self):
        node = LeafNode("a" ,"This is a link node", {"href": "https://www.boot.dev"})
        parento = ParentNode("div", [node])
        self.assertEqual(parento.to_html(), "<div><a href=https://www.boot.dev>This is a link node</a></div>")

    def test_multiple_children(self):
        child_node = LeafNode("p", "child")
        child_node2 = LeafNode("p", "child2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><p>child</p><p>child2</p></div>")

    def test_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")


    def test_text(self):
        node = TextNode("This is a text node", TextType.Plain_text)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.Bold)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.Plain_text)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.Images, "https://www.boot.dev")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.Bold)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


    def test_split_nodes_delimiter(self):
        node = TextNode("This is a *text* node", TextType.Plain_text)
        new_nodes = split_nodes_delimiter([node], "*", TextType.Bold)
        self.assertEqual(print(new_nodes), print([TextNode("This is a ", TextType.Plain_text), TextNode("text", TextType.Bold), TextNode(" node", TextType.Plain_text)]))
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[1].text, "text")


    def test_split_nodes_delimiter(self):
        node = TextNode("This is a 'code block' 'word' elo 'ka'", TextType.Code)
        new_nodes = split_nodes_delimiter([node], "'", TextType.Code)
        self.assertEqual(print(new_nodes), print([TextNode("This is a ", TextType.Plain_text), TextNode("code block", TextType.Code), TextNode(" word", TextType.Plain_text)]))
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[1].text, "code block")

    def test_extract_markdown_images(self):
        text = "This is a ![image](https://www.boot.dev) text [linkin](https://www.boot.dev) [youtube](https://www.youtube.com)"
        img_matches, link_matches = extract_markdown_images(text)
        self.assertEqual(img_matches, [("image", "https://www.boot.dev")])
        self.assertEqual(print(img_matches), print([("image", "https://www.boot.dev")]))
        self.assertEqual(print(link_matches), print([("linkin", "https://www.boot.dev")]))

if __name__ == "__main__":
    unittest.main()
