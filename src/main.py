# Hello, world!
from textnode import TextNode, TextType
from static import copy_static, copy_all
from md_to_html import *

def main():
    text = TextNode("Hello, world!", "link", "https://www.boot.dev")
    print(text)
    copy_static()
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
