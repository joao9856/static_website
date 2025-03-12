

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