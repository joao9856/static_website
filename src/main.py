from textnode import TextNode, TextType, split_nodes_delimiter

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD) 

    print(new_nodes)
if __name__ == "__main__":
    main()
