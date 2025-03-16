from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleanblock = []
    for block in blocks:
        if block != "":
            subblocks = block.split("\n")
            cleansub = ""
            for sub in subblocks:
                if sub != "":
                    cleansub += "\n" + sub.strip()
            cleansub = cleansub.strip("\n")
            if cleansub != "":
                cleanblock.append(cleansub)
    return cleanblock

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    if lines[0].startswith("```") and lines[-1].startswith("```") and len(lines) > 1:
        return BlockType.CODE
    q = 1
    u = 1
    o = 1
    for line in lines:
        if line.startswith(">"):
            q += 1
            if q == len(lines):
                return BlockType.QUOTE
        if line.startswith("- "):
            u += 1
            if u == len(lines):
                return BlockType.ULIST
        if line.startswith(f"{o}. "):
            o += 1
            if o == len(lines):
                return BlockType.OLIST
    return BlockType.PARAGRAPH

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    raise ValueError("No H1 title present")