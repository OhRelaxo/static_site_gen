from textnode import TextType, TextNode

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
            raise Exception("invalid Markdown syntax")
        if current_text[:-1]:
            new_nodes.append(TextNode(current_text[:-1], node.text_type))
    return new_nodes