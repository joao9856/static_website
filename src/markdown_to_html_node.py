from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType
from textnode import text_to_textnodes, text_node_to_html_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        granchildren = []
        if blocktype == BlockType.CODE:
            granchildren.append(LeafNode("code", block.strip("```").lstrip("\n")))
            children.append(ParentNode("pre", granchildren))
            continue
        lines = block.split("\n")
        for line in lines:
            greatgranchildren = text_to_html_node(line[2:])
            if blocktype == BlockType.QUOTE:                    
                granchildren.append(LeafNode(None, greatgranchildren))
                continue
            if blocktype == BlockType.OLIST:
                greatgranchildren = text_to_html_node(line[3:])    
            if blocktype in (BlockType.ULIST, BlockType.OLIST):
                granchildren.append(LeafNode("li", greatgranchildren.rstrip()))
                continue
            if blocktype == BlockType.HEADING:
                hlevel = line[:6].count("#")
                greatgranchildren = text_to_html_node(line[hlevel+1:])
                granchildren.append(LeafNode(None, greatgranchildren))
                continue
            if blocktype == BlockType.PARAGRAPH:
                greatgranchildren = text_to_html_node(line)
                granchildren.append(LeafNode(None, greatgranchildren))
                continue
        tmp = granchildren[-1].value.rstrip()
        granchildren[-1].value = tmp 
        if blocktype == BlockType.QUOTE:
            children.append(ParentNode("blockquote", granchildren))
        if blocktype == BlockType.ULIST:
            children.append(ParentNode("ul", granchildren))
        if blocktype == BlockType.OLIST:
            children.append(ParentNode("ol", granchildren))
        if blocktype == BlockType.HEADING:
            children.append(ParentNode(f"h{block[:6].count("#")}", granchildren))
        if blocktype == BlockType.PARAGRAPH:
            children.append(ParentNode("p", granchildren))
    return ParentNode("div", children)


def text_to_html_node(text):
    text_node = text_to_textnodes(text)
    greatgranchildren = ""
    for node in text_node:
        greatgranchildren += text_node_to_html_node(node).to_html()
    return greatgranchildren + " "