import re
from textnode import *

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            pieces = node.text.split(delimiter)
            if len(pieces) % 2 == 0:
                raise ValueError("Invalid markdown: unmatched delimiters")
            index = 0
            for piece in pieces:
                if index % 2 == 0:
                    result.append(TextNode(piece, TextType.TEXT))
                elif index % 2 != 0:
                    result.append(TextNode(piece, text_type))
                index += 1
        else:
            result.append(node)
    return result

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            result.append(node)
        else:
            current_text = node.text
            for match in matches:
                image_text = match[0]
                url = match[1]
                full_image = f"![{image_text}]({url})"
                sections = current_text.split(full_image, 1)
                if len(sections) != 2:
                    raise ValueError("Invalid markdown, image section not closed")
                if sections[0]:
                    result.append(TextNode(sections[0], node.text_type))
                result.append(TextNode(image_text, TextType.IMAGE, url))
                current_text = sections[1]               
            if current_text:
                result.append(TextNode(current_text, node.text_type))
    return result


def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            result.append(node)
        else:
            current_text = node.text
            for match in matches:
                link_text = match[0]
                url = match[1]
                full_link = f"[{link_text}]({url})"
                sections = current_text.split(full_link, 1)
                if len(sections) != 2:
                    raise ValueError("Invalid markdown, link section not closed")
                if sections[0]:
                    result.append(TextNode(sections[0], node.text_type))
                result.append(TextNode(link_text, TextType.LINK, url))
                current_text = sections[1]               
            if current_text:
                result.append(TextNode(current_text, node.text_type))
    return result

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches