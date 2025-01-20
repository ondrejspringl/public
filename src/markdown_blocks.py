from htmlnode import *
from textnode import *
from inline_markdown import *

block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"
block_type_paragraph = "paragraph"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        result.append(block)
    return result

def block_to_block_type(block):
    if is_heading(block):
        return block_type_heading
    if is_code_block(block):
        return block_type_code
    
    lines = block.split("\n")

    if is_quote_block(lines):
        return block_type_quote
    if is_unordered_list(lines):
        return block_type_unordered_list
    if is_ordered_list(lines):
        return block_type_ordered_list
    
    return block_type_paragraph
            
def is_heading(block):
    return block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### "))

def is_code_block(block):
    return block.startswith("```") and block.endswith("```")

def is_quote_block(lines):
    return all(line.startswith(">") for line in lines)

def is_unordered_list(lines):
    return all(line.startswith(("* ", "- ")) for line in lines)

def is_ordered_list(lines):
    line_number = 0
    for line in lines:
        line_number += 1
        if not line.startswith(f"{line_number}. "):
            return False
    return True

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        child = text_node_to_html_node(text_node)
        children.append(child)
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_quote:
            lines = block.split("\n")
            quote_text = " ".join(line.lstrip(">").strip() for line in lines)
            quote_node = ParentNode("blockquote", text_to_children(quote_text))
            children.append(quote_node)
        elif block_type == block_type_paragraph:
            lines = block.split("\n")
            block_text = " ".join(lines)
            paragraph_node = ParentNode("p",text_to_children(block_text))
            children.append(paragraph_node)
        elif block_type == block_type_heading:
            counter = 0
            for char in block:
                if char == "#":
                    counter += 1
                else:
                    break
            header_text = block.lstrip("#").strip()
            header_node = ParentNode(f"h{counter}", text_to_children(header_text))
            children.append(header_node)
        elif block_type == block_type_code:
            if block.startswith("```"):
                lines = block.split("\n")
                code_text = "\n".join(lines[1:-1])
            else:
                lines = block.split("\n")
                code_text = "\n".join(line[4:] if line.startswith("    ") else line for line in lines)
            code_node = ParentNode("code", [ParentNode(None, code_text)])
            pre_node = ParentNode("pre", [code_node])
            children.append(pre_node)
        elif block_type == block_type_unordered_list:
            list_items = []
            lines = block.split("\n")
            for line in lines:
                item_text = line.lstrip("*- ")
                li_node = ParentNode("li", text_to_children(item_text))
                list_items.append(li_node)
            list_node = ParentNode("ul", list_items)
            children.append(list_node)
        elif block_type == block_type_ordered_list:
            list_items = []
            lines = block.split("\n")
            for line in lines:
                item_text = line.lstrip("0123456789. ")
                li_node = ParentNode("li", text_to_children(item_text))
                list_items.append(li_node)
            list_node = ParentNode("ol", list_items)
            children.append(list_node)
    return ParentNode("div", children)