from textnode import TextType, TextNode
import re

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
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
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

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
        if not extracted_markdown:
            new_nodes.append(node)
            continue
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
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    if new_nodes:
        return new_nodes
    return old_nodes

def extract_title(markdown):
    header = markdown.split("\n", 1)
    header = header[0].split(" ", 1)
    if header[0] == "#":
        return header[1]
    raise ValueError("wrong header")