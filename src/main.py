from textnode import TextNode
from block_conv import markdown_to_htmlnode, markdown_to_blocks
from htmlnode import HTMLNode
import os
import shutil
from pathlib import Path


def transfer_files(source_path, dest_path):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)
    if os.path.exists(source_path):
        directory_contents = os.listdir(source_path)
        for p in directory_contents:
            file_path = os.path.join(source_path, p)
            if os.path.isfile(file_path):
                shutil.copy(file_path, dest_path)
            else:
                joined_dest = os.path.join(dest_path, p)
                transfer_files(file_path, joined_dest)
    else:
        raise Exception("Invalid path to source directory")

def extract_title(markdown):
    md_lines = markdown.split("\n")
    for line in md_lines:
        if line.startswith("# "):
            title_line = line
            break
    if not title_line:
        raise Exception("No title line")
    title_line_text = title_line.split("# ")[1]
    return title_line_text

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        contents = f.read()
    
    with open(template_path, "r") as temp_f:
        template_contents = temp_f.read()
    

    html_node = markdown_to_htmlnode(contents)
    html_string = html_node.to_html()
    website_title = extract_title(contents)
    adding_title = template_contents.replace("{{ Title }}", website_title)
    final_html = adding_title.replace("{{ Content }}", html_string)

    dir_name = os.path.dirname(dest_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(dest_path, "w") as f_web_file:
        f_web_file.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    contents_files = os.listdir(dir_path_content)
    for f in contents_files:
        cur_path = os.path.join(dir_path_content, f)
        joined_dest_path = os.path.join(dest_dir_path, f)
        if os.path.isfile(cur_path) and cur_path.endswith(".md"):
            updated_dest_path = Path(joined_dest_path).with_suffix(".html")
            generate_page(cur_path, template_path, updated_dest_path)
        else:

            dest_path = os.path.join(dest_dir_path, f)
            generate_pages_recursive(cur_path, template_path, dest_path)


def main():
    # test_node = TextNode("Test text", "text")
    # print(repr(test_node))

    transfer_files("static/", "public/")
    generate_pages_recursive("content/", "template.html", "public/")

main()