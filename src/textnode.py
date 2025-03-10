from enum import Enum
from htmlnode import LeafNode
from extract_markdown import extract_markdown_images, extract_markdown_links

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, other):
        return (self.text == other.text and self.text_type == other.text_type and self.url == other.url)  
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type not in (TextType.TEXT, TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.LINK, TextType.IMAGE):
        raise Exception(f"{text_node.text_type} is not a valid text type")
    if text_node.text_type == TextType.TEXT:
        return LeafNode(value=text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        if text_node.url == None:
            raise ValueError("url should be set for a LINK type")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        if text_node.url == None:
            raise ValueError("url should be set for an IMAGE type")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter not in ("`", "**", "_"):
        raise ValueError("Not a valid Markdown delimiter")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            raise ValueError(f"No markdown in text for indicated delimiter.")
        node_text = node.text.split(delimiter)
        for text in node_text:
            if f"{delimiter}{text.strip()}{delimiter}" in node.text:           
                new_nodes.append(TextNode(text, text_type))
            elif text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        image = extract_markdown_images(node.text)
        image_alt = []
        image_link = []
        for item in image:
            image_alt.append(item[0])
            image_link.append(item[1])
        node_text = node.text.split(f"![{image_alt[0]}]({image_link[0]})")
        for i in range(len(image_alt)):
            if node_text[0] == "":           
                new_nodes.append(TextNode(image_alt[i], TextType.IMAGE, image_link[i]))
                node_text.pop(0)
                if i+1 != len(image_alt):
                    node_copy = node_text.copy()
                    node_text = node_copy[0].split(f"![{image_alt[i+1]}]({image_link[i+1]})")
                elif node_text[0] != "":
                    new_nodes.append(TextNode(node_text[0], TextType.TEXT))
                continue
            if node_text[0][-1:] == " " and node_text[1][:1] == " ":
                new_nodes.append(TextNode(node_text[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt[i], TextType.IMAGE, image_link[i]))
                node_text.pop(0)
                if i+1 != len(image_alt):
                    node_copy = node_text.copy()
                    node_text = node_copy[0].split(f"![{image_alt[i+1]}]({image_link[i+1]})")
                else:
                    new_nodes.append(TextNode(node_text[0], TextType.TEXT))
                continue
            if node_text[1] == "":           
                new_nodes.append(TextNode(node_text[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt[i], TextType.IMAGE, image_link[i]))
    return new_nodes





def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        image = extract_markdown_links(node.text)
        link_alt = []
        link_link = []
        for item in image:
            link_alt.append(item[0])
            link_link.append(item[1])
        node_text = node.text.split(f"![{link_alt[0]}]({link_link[0]})")
        for i in range(len(link_alt)):
            if node_text[0] == "":           
                new_nodes.append(TextNode(link_alt[i], TextType.LINK, link_link[i]))
                node_text.pop(0)
                if i+1 != len(link_alt):
                    node_copy = node_text.copy()
                    node_text = node_copy[0].split(f"![{link_alt[i+1]}]({link_link[i+1]})")
                elif node_text[0] != "":
                    new_nodes.append(TextNode(node_text[0], TextType.TEXT))
                continue
            if node_text[0][-1:] == " " and node_text[1][:1] == " ":
                new_nodes.append(TextNode(node_text[0], TextType.TEXT))
                new_nodes.append(TextNode(link_alt[i], TextType.LINK, link_link[i]))
                node_text.pop(0)
                if i+1 != len(link_alt):
                    node_copy = node_text.copy()
                    node_text = node_copy[0].split(f"![{link_alt[i+1]}]({link_link[i+1]})")
                else:
                    new_nodes.append(TextNode(node_text[0], TextType.TEXT))
                continue
            if node_text[1] == "":           
                new_nodes.append(TextNode(node_text[0], TextType.TEXT))
                new_nodes.append(TextNode(link_alt[i], TextType.LINK, link_link[i]))
    return new_nodes