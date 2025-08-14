from enum import Enum

class BlcokType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    new_markdown = markdown.split("\n\n")
    clean_markdown = []
    for text in new_markdown:
        if not text:
            continue
        clean_markdown.append(text.strip())
    return clean_markdown

def block_to_block_type(markdown_block: str):
    if not markdown_block:
        return None
    block_list = markdown_block.split(" ")
    split_test = markdown_block.split("\n")
    print(split_test.split(" "))
    first_chars = block_list[0]
    last_chars = block_list[-1]
    if "#" in first_chars:
        return BlcokType.HEADING
    if "```" in first_chars and "```" in last_chars:
        return BlcokType.CODE

