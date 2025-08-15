import os
from markdown_to_html import markdown_to_html_node
from inline_markdown import extract_title
from copystatic import copy_content


def main():
    working_dir = os.getcwd()
    content_path = os.path.join(working_dir, "content")
    public_dir = os.path.join(working_dir, "public")
    template_path = os.path.join(working_dir, "template.html")
    copy_content()
    generate_pages_recursive(content_path, template_path, public_dir)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open (from_path, encoding="utf-8") as f:
        markdown = f.read()
    f.close()
    with open(template_path, encoding="utf-8") as f:
        template = f.read()
    f.close()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    title = extract_title(markdown)
    template= template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as new_html_page:
        new_html_page.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files = os.listdir(dir_path_content)
    for file in files:
        if os.path.isdir(os.path.join(dir_path_content, file)):
            new_dir_path_content = os.path.join(dir_path_content, file)
            new_dest_dir_path = os.path.join(dest_dir_path, file)
            generate_pages_recursive(new_dir_path_content, template_path, new_dest_dir_path)
        else:
            dest_file = file.strip(".md")
            dest_file += ".html"
            new_dest_dir_path = os.path.join(dest_dir_path, dest_file)
            new_dir_path_content = os.path.join(dir_path_content, file)
            generate_page(new_dir_path_content, template_path, new_dest_dir_path)



main()