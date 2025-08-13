
from enum import Enum

class TextType(Enum):
    text = "text"
    bold = "**Bold text**"
    italic = "_Italic text_"
    code = "`Code text`"
    link = "link"
    image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url # None is the Default value

    def __eq__(self, other):
        return(
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"