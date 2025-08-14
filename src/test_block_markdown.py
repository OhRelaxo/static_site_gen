import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_block_type_code(self):
        block = markdown_to_blocks("""
        ```
        This is Code
        ```
        """)
        self.assertEqual(BlockType.CODE, block_to_block_type(block[0]))

    def test_block_type_bad_ordered_list(self):
        block = markdown_to_blocks("""
        b. This is the first list item in a list block
        c. This is a list item
        a. This is another list item
        """)
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block[0]))

    def test_block_type_bad_ordered_list_two(self):
        block = markdown_to_blocks("""
        1. This is the first list item in a list block
        4. This is a list item
        2. This is another list item
        """)
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block[0]))

    def test_block_type_quote(self):
        block = markdown_to_blocks("""
> This is the first list item in a list block
> This is a list item
> This is another list item
        """)
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block[0]))

    def test_block_type_bad_quote(self):
        block = markdown_to_blocks("""
        > This is the first list item in a list block
        - This is a list item
        > This is another list item
        """)
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block[0]))

    def test_block_type_unordered_list(self):
        block = markdown_to_blocks("""
- This is the first list item in a list block
- This is a list item
- This is another list item
        """)
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block[0]))

    def test_block_type_bad_unordered_list(self):
        block = markdown_to_blocks("""
        - This is the first list item in a list block
        - This is a list item
        - This is another list item
        This is not an unordered list anymore""")
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block[0]))

    def test_block_type_heading(self):
        block = markdown_to_blocks("""# This is a heading""")
        self.assertEqual(BlockType.HEADING, block_to_block_type(block[0]))

    def test_block_type_paragraph(self):
        block = markdown_to_blocks("""This is a paragraph""")
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block[0]))



if __name__ == "__main__":
    unittest.main()