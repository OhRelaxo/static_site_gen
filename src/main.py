from textnode import TextNode, TextType, split_nodes_delimiter

def main():
    node = TextNode("This is **a lot of bold text** **hallo** hallo", TextType.TEXT)
    new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
    print(new_node)

main()