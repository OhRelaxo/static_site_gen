import os
from markdown_to_html import markdown_to_html_node
from inline_markdown import extract_title, split_nodes_link, TextNode, TextType
from copystatic import copy_content


def main():
    working_dir = os.getcwd()
    content_path = os.path.join(working_dir, "content/index.md")
    public_dir = os.path.join(working_dir, "public/index.html")
    template_path = os.path.join(working_dir, "template.html")
    copy_content()
    generate_page(content_path, template_path, public_dir)

    with open (content_path, encoding="utf-8") as f:
        markdown = f.read()
    f.close()

    #print(split_nodes_link([TextNode(markdown, TextType.TEXT)]))


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

    with open(dest_path, "w") as new_html_page:
        new_html_page.write(template)



main()