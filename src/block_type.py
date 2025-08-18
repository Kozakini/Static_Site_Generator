from enum import Enum


class BlockType(Enum):
    Paragraph = "paragraph"
    Header = "header"
    Code = "code"
    Quote = "quote"
    Ordered_list = "ordered_list"
    Unordered_list = "unordered_list"


def block_to_block_type(markdown_block):
    if markdown_block.startswith("#"):
        return BlockType.Header
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.Code
    elif markdown_block.startswith(">"):
        return BlockType.Quote
    elif markdown_block.startswith("-"):
        return BlockType.Unordered_list
    elif markdown_block.startswith("1. "):
        i = 1
        for line in markdown_block.split("\n"):
            if not line.startswith(f"{i}. "):
                return BlockType.Paragraph
            i += 1
        return BlockType.Ordered_list
    else:
        return BlockType.Paragraph
