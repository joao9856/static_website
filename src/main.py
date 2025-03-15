from textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
import os, shutil


def static_to_public():
    public_path = os.path.join(os.getcwd(), "public")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
        os.mkdir(public_path)
    else:
        os.mkdir(public_path)
    static_path = os.path.join(os.getcwd(), "static")
    copy_to_public(static_path, public_path)


def copy_to_public(from_path, to_path):
    for path in os.listdir(from_path):
        if os.path.isfile(os.path.join(from_path, path)):
            shutil.copy(os.path.join(from_path, path), os.path.join(to_path, path))
            continue
        os.mkdir(os.path.join(to_path, path))
        copy_to_public(os.path.join(from_path, path), os.path.join(to_path, path))

        
def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    print(os.path.dirname(__file__))
    print(type(os.path.dirname(__file__)))
    print(os.listdir(os.getcwd()))
    static_to_public()
if __name__ == "__main__":
    main()
