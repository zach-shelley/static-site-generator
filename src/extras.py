from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise Exception("Not a TextNode")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split_elements = node.text.split(delimiter)
        # Does is there an opening and closing de-limiter? No nested elements
        if len(split_elements) % 2 == 0:
            raise Exception("Invalid markdown syntax")
        
        elif len(split_elements) == 1:
            new_nodes.append(node)
            continue

        for i, el in enumerate(split_elements):
            if i % 2 != 0:
                new_nodes.append(TextNode(el, text_type))
            else:
                new_nodes.append(TextNode(el, "text"))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise Exception("Not a TextNode")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        remaining = node.text
        for img in images:
            image_alt, image_link = img
            split_text = remaining.split(f"![{image_alt}]({image_link})", 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], "text"))
            new_nodes.append(TextNode(image_alt, "image", image_link))
            remaining = split_text[1]
        if remaining:
            new_nodes.append(TextNode(remaining, "text"))
    return new_nodes
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise Exception("Not a TextNode")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        remaining = node.text
        for link in links:
            link_text, link_url = link
            split_text = remaining.split(f"[{link_text}]({link_url})", 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], "text"))
            new_nodes.append(TextNode(link_text, "link", link_url))
            remaining = split_text[1]
        if remaining:
            new_nodes.append(TextNode(remaining, "text"))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, "text")]
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "_", "italic")
    nodes = split_nodes_delimiter(nodes, "`", "code")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)