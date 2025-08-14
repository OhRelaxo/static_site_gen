from enum import Enum

class BlockType(Enum):
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
    first_chars = block_list[0]
    last_chars = block_list[-1]
    if "#" in first_chars:
        return BlockType.HEADING
    if "```" in first_chars and "```" in last_chars:
        return BlockType.CODE
    count = 0
    count_type = 0
    last_type = None
    block_list = markdown_block.split("\n")
    for line in block_list:
        char = line.split(" ")
        if "-" in char[0]:
            if last_type is None or last_type == BlockType.UNORDERED_LIST:
                last_type = BlockType.UNORDERED_LIST
                count_type += 1
            else:
                return BlockType.PARAGRAPH

        if ">" in char[0]:
            if last_type is None or last_type == BlockType.QUOTE:
                last_type = BlockType.QUOTE
                count_type += 1
            else:
                return BlockType.PARAGRAPH

        if "." in char[0]:
            if last_type is None or last_type == BlockType.ORDERED_LIST:
                last_type = BlockType.ORDERED_LIST
                count_type += 1
                number = char[0].strip(".")
                if type(number) is not int:
                    return BlockType.PARAGRAPH
                    #raise ValueError("ordered list needs a number")
                if count + 1 == number:
                    count = number
                else:
                    return BlockType.PARAGRAPH
                    #raise ValueError("ordered list needs to be properly ordered")
            else:
                return BlockType.PARAGRAPH

    if count_type == len(block_list):
        return last_type
    else:
        return BlockType.PARAGRAPH
