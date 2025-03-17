from textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
import os, shutil, sys
from markdown_to_html_node import markdown_to_html_node
from markdown_to_blocks import extract_title

basepath = sys.argv[1]

def static_to_public():
    public_path = os.path.join(os.getcwd(), "docs")
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

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    htmlstring = markdown_to_html_node(markdown).to_html()
    new_page = template.replace("{{ Title }}", extract_title(markdown)).replace("{{ Content }}", htmlstring).replace('src="/', f'src="{basepath}').replace('href="/', f'href="{basepath}')
    split_path = dest_path.split("/")
    base_path = os.getcwd()
    for path in split_path:
        if path not in base_path:
            base_path = os.path.join(base_path, path)
            if os.path.exists(base_path) == False and base_path != dest_path:
                os.mkdir(base_path)
    with open(dest_path, "w") as f:
        f.write(new_page)

def content_checker(base_from, base_dest):
    paths = []
    for path in os.listdir(base_from):
        if os.path.isfile(os.path.join(base_from, path)):
            if path.endswith(".md"):
                paths.append([os.path.join(base_from, path), os.path.join(base_dest, path.replace(".md", ".html"))])
            continue
        if os.path.isdir(os.path.join(base_from, path)):
            paths.extend(content_checker(os.path.join(base_from, path), os.path.join(base_dest, path)))
    return paths
        
        
def main():
    #node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #print(node)
    #print(os.path.dirname(__file__))
    #print(type(os.path.dirname(__file__)))
    #print(os.listdir(os.getcwd()))
    global basepath
    print(basepath, "debug")
    if basepath == "":
        basepath = "/"
    

    static_to_public()
    
    base_from = os.path.join(os.getcwd(), "content")
    template = os.path.join(os.getcwd(), "template.html")
    base_dest = os.path.join(os.getcwd(), "docs")
    
    paths = content_checker(base_from, base_dest)
    
    for path in paths:
        generate_page(path[0], template, path[1], basepath)
if __name__ == "__main__":
    main()
