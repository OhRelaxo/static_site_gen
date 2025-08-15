
class HTMLNode:

    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag #A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value #A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children #A list of HTMLNode objects representing the children of this node
        self.props = props #A dictionary of key-value pairs representing the attributes of the HTML tag.

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        to_html = f""
        if self.props:
            for key, value in self.props.items():
                to_html += f""" {key}="{value}" """
        return to_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
        #nicht self.children

    def to_html(self):
        if self.value:
            if self.tag:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            return self.value
        raise ValueError("invalid HTML: no value")

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag:
            if self.children:
                html = f"<{self.tag}>"
                for child in self.children:
                    try:
                        new_html = child.to_html()
                    except Exception as e:
                        print(e)
                        continue
                    html += new_html
                return f"{html}</{self.tag}>"
            raise ValueError("invalid HTML: no children")
        raise ValueError("invalid HTML: no tag")
