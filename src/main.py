from textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_image

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD) 

    node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) ![image2](https://i.imgur.com/zjjcJKZ2.png) ![second image](https://i.imgur.com/3elNhQu.png) ![second image2](https://i.imgur.com/3elNhQu2.png)",
            TextType.TEXT,
        )
    new_nodes = split_nodes_image([node])

    print(new_nodes)
if __name__ == "__main__":
    main()
