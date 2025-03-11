from textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    new_nodes = text_to_textnodes(text)
    print(new_nodes)
if __name__ == "__main__":
    main()
