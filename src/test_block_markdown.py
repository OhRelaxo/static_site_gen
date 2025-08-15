import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from markdown_to_html import markdown_to_html_node


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

        def test_paragraph(self):
            md = """
    This is **bolded** paragraph
    text in a p
    tag here

    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
            )

        def test_paragraphs(self):
            md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

        def test_lists(self):
            md = """
    - This is a list
    - with items
    - and _more_ items

    1. This is an `ordered` list
    2. with items
    3. and more items

    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
            )

        def test_headings(self):
            md = """
    # this is an h1

    this is paragraph text

    ## this is an h2
    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
            )

        def test_blockquote(self):
            md = """
    > This is a
    > blockquote block

    this is paragraph text

    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
            )

        def test_code(self):
            md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )



if __name__ == "__main__":
    unittest.main()