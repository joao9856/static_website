from textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
import os, shutil
from markdown_to_html_node import markdown_to_html_node
from markdown_to_blocks import extract_title


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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    htmlstring = markdown_to_html_node(markdown).to_html()
    new_page = template.replace("{{ Title }}", extract_title(markdown)).replace("{{ Content }}", htmlstring)
    split_path = dest_path.split("/")
    base_path = os.getcwd()
    for path in split_path:
        if path not in base_path:
            base_path = os.path.join(base_path, path)
            if os.path.exists(base_path) == False and base_path != dest_path:
                os.mkdir(base_path)
    with open(dest_path, "w") as f:
        f.write(new_page)
        
def main():
    #node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #print(node)
    #print(os.path.dirname(__file__))
    #print(type(os.path.dirname(__file__)))
    #print(os.listdir(os.getcwd()))
    static_to_public()
    generate_page(os.path.join(os.getcwd(), "content/index.md"), os.path.join(os.getcwd(), "template.html"), os.path.join(os.getcwd(), "public/index.html"))
if __name__ == "__main__":
    main()
