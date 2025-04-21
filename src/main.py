import os
import shutil
import sys

from markdownblocks import MarkdownBlock

def main():

    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    # Copy static files from static to public
    copy_static_files(output_dir)

    # Generate the page from content/index.md using template.html
    content_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content")
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "template.html")

    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                rel_path = os.path.relpath(from_path, content_dir)
                dest_path = os.path.join(output_dir, rel_path).replace(".md", ".html")

                generate_page(from_path, template_path, dest_path, base_path)

def copy_static_files(dest_dir):
    project_root = os.path.dirname(os.path.dirname(__file__))
    source_dir = os.path.join(project_root, "static")

    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return

    os.makedirs(dest_dir, exist_ok=True)

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            print(f"Copying file {source_path} to {dest_path}")
            shutil.copy(source_path, dest_path)
        elif os.path.isdir(source_path):
            print(f"Copying directory {source_path} to {dest_path}")
            shutil.copytree(source_path, dest_path)

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):  # H1 headers start with '# ' (with a space)
            return line[2:].strip()  # Return the title after the '# ' symbol, stripped of leading/trailing spaces
    raise ValueError("No H1 header found in markdown.")  # Raise an exception if no H1 header is found

def generate_page(from_path, template_path, dest_path, base_path):
    with open(from_path, 'r') as f:
        markdown_content = f.read()

    with open(template_path, 'r') as f:
        template_content = f.read()

    node = MarkdownBlock.markdown_to_html_node(markdown_content)
    html_content = node.to_html()
    title = extract_title(markdown_content)

    html_page = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Replace href/src root slashes with base_path
    html_page = html_page.replace('href="/', f'href="{base_path}')
    html_page = html_page.replace('src="/', f'src="{base_path}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(html_page)

    print(f"Page generated successfully at {dest_path}")
    
if __name__ == "__main__":
    main()
