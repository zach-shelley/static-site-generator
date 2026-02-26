from enum import Enum
from htmlnode import HTMLNode, text_node_to_html_node, ParentNode
from extras import text_to_textnodes
from textnode import TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_blocktype(block):
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        split_block = block.split("\n")
        for b in split_block:
            if not b.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        split_block = block.split("\n")
        for b in split_block:
            if not b.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block[0].isnumeric() and block.startswith("1. "):
        split_block = block.split("\n")
        for i, b in enumerate(split_block, 1):
            if not b.startswith(f"{i}."):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = [block.strip() for block in blocks if block]
    return cleaned_blocks

def markdown_to_htmlnode(markdown):
    cleaned_blocks = markdown_to_blocks(markdown)
    html_list = []
    for b in cleaned_blocks:
        blocktype = block_to_blocktype(b)
        if blocktype == BlockType.PARAGRAPH:
            cleaned_b = b.replace("\n", " ")
            nodes = text_to_textnodes(cleaned_b)
            html_nodes = [text_node_to_html_node(node) for node in nodes]
            html_list.append(ParentNode(tag="p", children=html_nodes))
        elif blocktype == BlockType.HEADING:
            count = 0
            for char in b:
                if char != "#":
                    break
                count += 1
            node_text = b.split(f"{'#' * count}")
            child_nodes = text_to_textnodes(node_text[1].strip())
            html_child_nodes = [text_node_to_html_node(node) for node in child_nodes]
            html_list.append(ParentNode(tag=f"h{count}", children=html_child_nodes))
        elif blocktype == BlockType.QUOTE:
            lines = b.split("\n")
            cleaned_quote = " ".join(line.lstrip(">").strip() for line in lines)
            text_nodes = text_to_textnodes(cleaned_quote)
            html_children = [text_node_to_html_node(node) for node in text_nodes]
            html_list.append(ParentNode(tag="blockquote", children=html_children))
            
        elif blocktype == BlockType.CODE:
            code_type_text = b.split("```")[1].lstrip("\n")
            textnode = TextNode(text=code_type_text, text_type="code")
            code_leaf_node = text_node_to_html_node(textnode)
            html_list.append(ParentNode("pre", children = [code_leaf_node]))
        
        elif blocktype == BlockType.UNORDERED_LIST:
            split_list = b.split("\n")
            li_nodes = []
            for n in split_list:
                cleaned_n = n.replace("- ", "")
                child_nodes = text_to_textnodes(cleaned_n)
                html_li_nodes = [text_node_to_html_node(node) for node in child_nodes]
                li_nodes.append(ParentNode("li", children=html_li_nodes))
            
            html_list.append(ParentNode(tag="ul", children=li_nodes))
        elif blocktype == BlockType.ORDERED_LIST:
            split_list = b.split("\n")
            li_nodes = []
            for n in split_list:
                list_counter = n.split(".", 1)
                cleaned_n = list_counter[1].strip()
                child_nodes = text_to_textnodes(cleaned_n)
                html_li_children = [text_node_to_html_node(node) for node in child_nodes]
                li_nodes.append(ParentNode("li", children=html_li_children))
        
            html_list.append(ParentNode("ol", children = li_nodes))

    return ParentNode(tag="div", children=html_list)
        
        
