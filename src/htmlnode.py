
from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented in parent class")
    
    def props_to_html(self):
        formatted_string = ""
        for key, value in self.props.items():
            formatted_string += f' {key}="{value}"'
        return formatted_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props)
    

    def to_html(self):
        if not self.tag:
            if not self.value:
                raise ValueError("Leaf node must have a value")
            return self.value
        props = self.props_to_html() if self.props else ""
        
        return f'<{self.tag}{props}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node requires tag")
        if not self.children:
            raise ValueError("Parent node must have children")
        
        nested_nodes = [child.to_html() for child in self.children]
        joined_string = "".join(nested_nodes)
        return f"<{self.tag}>{joined_string}</{self.tag}>"


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise Exception("Not a text node")
    
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag='i', value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src":text_node.url, "alt":text_node.text})