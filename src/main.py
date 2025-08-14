from block_markdown import markdown_to_blocks

def main():
    print(markdown_to_blocks("""# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""))
main()