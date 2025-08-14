from markdown_blocks import markdown_to_blocks, block_to_block_type

def main():
    text_blocks = markdown_to_blocks("""# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
This is still just a paragraph of text.

- This is the first list item in a list block
- This is a list item
- This is another list item""")

    text_block = markdown_to_blocks("""
        - This is the first list item in a list block
        - This is a list item
        - This is another list item
        """)
    print(text_block)
    print(block_to_block_type(text_block[0]))
main()