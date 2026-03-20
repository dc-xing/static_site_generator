from textnode import TextNode,TextType
from textblock import markdown_to_html_node
from extract import extract_title
from pathlib import Path

import os
import shutil


static_path = "./static"
public_path = "./public"
template_path = "./template.html"
content_path = "./content/"


def main():
    print("Deleting public directory")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    print("Copying static to public")
    static_to_public(static_path, public_path)
    generate_pages_recursive(content_path, template_path, public_path)


def static_to_public(from_path, dest_path):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    for filename in os.listdir(from_path):
        src_path = os.path.join(from_path, filename)
        dst_path = os.path.join(dest_path, filename)
        print(f"Copied {src_path} to {dst_path}")
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)        
        else:
            static_to_public(src_path, dst_path)       

def generate_page(content_path, template_path, public_path):     
    print(f"Generating page from {content_path} to {public_path} using {template_path}")  
    with open(content_path, 'r') as f:
        markdown_content = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    html_title = extract_title(markdown_content)
    final_content = template.replace("{{ Content }}", html_content)
    final_content = final_content.replace("{{ Title }}", html_title)
    dest_dir = os.path.dirname(public_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(public_path, 'w') as f:
        f.write(final_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, filename)
        dst_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(src_path) and src_path.endswith(".md"):
            dst_path = Path(dst_path).with_suffix('.html')
            generate_page(src_path, template_path, dst_path)
        elif os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dst_path)
    



main()