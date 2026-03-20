from enum import Enum
from htmlnode import LeafNode, ParentNode, HTMLNode
from textnode import TextNode, TextType,text_node_to_html_node
from splitnodes import text_to_textnodes

import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = []
    raw_blocks = markdown.split('\n\n') # Split by double newlines to separate blocks

    for block in raw_blocks:
        block = block.strip() # Remove leading and trailing whitespace
        if block: # Only add non-empty blocks
            blocks.append(block)
    return blocks


def block_to_block_type(block):
    lines = block.split('\n')

    if re.fullmatch(r'#{1,6} .+', block):
        return BlockType.HEADING
    if re.fullmatch(r'```\n.*?\n?```', block, flags=re.DOTALL):
        return BlockType.CODE
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    if all(re.fullmatch(rf'^{i}\. .+', line) for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
  
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        html_node = block_to_html_node(block)
        html_nodes.append(html_node)
    return ParentNode("div", html_nodes, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return head_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    elif block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    raise ValueError(f"Unknown BlockType: {block_type}")

def text_to_children(block):
    text_nodes = text_to_textnodes(block)
    children_nodes = []
    for text_node in text_nodes:
        children_nodes.append(text_node_to_html_node(text_node))
    return children_nodes

def paragraph_to_html_node(block):
    text = block.replace('\n', ' ')
    children_nodes = text_to_children(text)
    return ParentNode("p", children_nodes)

def head_to_html_node(block):
    match = re.match(r'^(#{1,6}) (.+)$', block)
    if not match:
        raise ValueError("Invalid heading markdown")
    level = len(match.group(1))
    content = match.group(2)
    children_nodes = text_to_children(content)
    return ParentNode(f"h{level}", children_nodes)

def code_to_html_node(block):
    match = re.match(r'^```\n(.*?\n?)```$', block, flags=re.DOTALL)
    if not match:
        raise ValueError("Invalid code markdown")
    content = match.group(1)
    raw_text_node = TextNode(content, TextType.TEXT)
    chaild_node = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [chaild_node])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split('\n')
    new_lines = []
    for line in lines:
        if not line.startswith('>'):
            raise ValueError("Invalid quote markdown")
        new_lines.append(line.lstrip('>').strip())
    content = ' '.join(new_lines)
    children_nodes = text_to_children(content)
    return ParentNode("blockquote", children_nodes)

def unordered_list_to_html_node(block):
    items = block.split('\n')
    html_items = []
    for item in items:
        content = item[2:]
        children = text_to_children(content)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def ordered_list_to_html_node(block):
    items = block.split('\n')
    html_items = []
    for item in items:
        parts = item.split('. ', 1)
        content = parts[1]
        children = text_to_children(content)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)