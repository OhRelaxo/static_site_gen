from markdown_to_html import markdown_to_html_node

def main():
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

    node = markdown_to_html_node(md)
    md2 = """# This is a test"""
    print(node.to_html())
main()