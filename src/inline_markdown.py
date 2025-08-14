from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes: list, delimiter, text_type):
    new_nodes = []
    current_text = ""
    delimiter_found = False
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split = node.text.split(" ")
        for string in split:
            if delimiter in string:
                if current_text and delimiter_found == False and delimiter not in current_text:
                    new_nodes.append(TextNode(current_text, node.text_type))
                    current_text = " "

                if delimiter in string.lstrip(delimiter) and delimiter in string.rstrip(delimiter):
                    clean = string.replace(delimiter, "")
                    new_nodes.append(TextNode(clean, text_type))
                    current_text = " "
                elif delimiter_found:
                    current_text += string.rstrip(delimiter)
                    new_nodes.append(TextNode(current_text, text_type))
                    current_text = " "
                    delimiter_found = False
                else:
                    current_text = string.lstrip(delimiter) + " "
                    delimiter_found = True
            else:
                current_text += string + " "
        if delimiter_found:
            raise ValueError("invalid Markdown syntax at the delimiter")
        if current_text[:-1]:
            new_nodes.append(TextNode(current_text[:-1], node.text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    return split_nodes_helper(old_nodes, True)

def split_nodes_link(old_nodes):
    return split_nodes_helper(old_nodes, False)

def split_nodes_helper(old_nodes, image:bool):
    new_nodes = []
    i = 0
    if image:
        text_type = TextType.IMAGE
    else:
        text_type = TextType.LINK
    for node in old_nodes:
        original_text = node.text
        if not original_text:
            continue
        if image:
            extracted_markdown = extract_markdown_images(original_text)
        else:
            extracted_markdown = extract_markdown_links(original_text)
        while i <= len(extracted_markdown) - 1:
            image_alt = extracted_markdown[i][0]
            image_link = extracted_markdown[i][1]
            if image:
                sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            else:
                sections = original_text.split(f"[{image_alt}]({image_link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, text_type, image_link))
            original_text = sections.pop()
            i += 1
    if new_nodes:
        return new_nodes
    return old_nodes