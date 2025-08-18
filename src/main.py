# Hello, world!
from textnode import TextNode, TextType
from static import copy_static, copy_all
from md_to_html import *
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath= sys.argv[1]

    copy_static()
    generate_pages_recursive("content", "template.html", "docs", basepath)



if __name__ == "__main__":
    main()
