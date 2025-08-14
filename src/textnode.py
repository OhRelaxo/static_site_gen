from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text: str = text
        self.text_type = TextType(text_type)
        self.url: str = url # None is the Default value

    def __eq__(self, other):
        return(
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")
    raise ValueError(f"invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes: list, delimiter, text_type):
    new_nodes = []
    current_text = ""
    delimiter_found = False
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splited = node.text.split(" ")
        for string in splited:
            if delimiter in string:
                #print(string)
                # wenn nicht, dann erstellen wir zwar den neuen TextNode aber noch nicht den für den text typen
                if current_text and delimiter_found == False and delimiter not in current_text:
                    new_nodes.append(TextNode(current_text, node.text_type))
                    current_text = " "

                if delimiter in string.lstrip(delimiter) and delimiter in string.rstrip(delimiter):
                    clean = string.replace(delimiter, "")
                    new_nodes.append(TextNode(clean, text_type))
                elif delimiter_found:
                    current_text += string.rstrip(delimiter)
                    new_nodes.append(TextNode(current_text, text_type))
                    current_text = " "
                    delimiter_found = False
                else:
                    current_text = string.lstrip(delimiter) + " "
                    #print(current_text)
                    delimiter_found = True
            else:
                current_text += string + " "
        if delimiter_found:
            raise Exception("invalid Markdown syntax")
        if current_text[:-1]:
            new_nodes.append(TextNode(current_text[:-1], node.text_type))
    return new_nodes