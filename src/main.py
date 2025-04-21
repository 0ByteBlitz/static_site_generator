import os
import shutil

from markdownblocks import MarkdownBlock

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    
    # Copy static files from static to public
    copy_static_files()

    # Generate the page from content/index.md using template.html
    # Define content and template paths
    project_root = os.path.dirname(os.path.dirname(__file__))
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")

    # Generate pages from all markdown files
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                rel_path = os.path.relpath(from_path, content_dir)
                dest_path = os.path.join(project_root, "public", rel_path).replace(".md", ".html")

                generate_page(from_path, template_path, dest_path)

def copy_static_files():
    # Copy from source (static) to destination (public)
    project_root = os.path.dirname(os.path.dirname(__file__))
    source_dir = os.path.join(project_root, "static")
    dest_dir = os.path.join(project_root, "public")

    # Check if the source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return

    # Ensure the destination directory exists (recreate it if needed)
    if os.path.exists(dest_dir):
        # If the directory exists, remove it before recreating
        shutil.rmtree(dest_dir)
    
    # Create the destination directory
    os.makedirs(dest_dir)

    # Now copy the files from source to destination
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            print(f"Copying file {source_path} to {dest_path}")
            shutil.copy(source_path, dest_path)
        elif os.path.isdir(source_path):
            print(f"Copying directory {source_path} to {dest_path}")
            shutil.copytree(source_path, dest_path)

    print(f"Static files copied from {source_dir} to {dest_dir}")

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):  # H1 headers start with '# ' (with a space)
            return line[2:].strip()  # Return the title after the '# ' symbol, stripped of leading/trailing spaces
    raise ValueError("No H1 header found in markdown.")  # Raise an exception if no H1 header is found

def generate_page(from_path, template_path, dest_path):
    # Print a message indicating the process
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()

    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Use the markdown_to_html_node function to convert markdown to HTML (assuming the function exists)
    node = MarkdownBlock.markdown_to_html_node(markdown_content)
    html_content = node.to_html()

    # Use the extract_title function to get the page title
    title = extract_title(markdown_content)

    # Replace placeholders in the template
    html_page = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the generated HTML to the destination file
    with open(dest_path, 'w') as f:
        f.write(html_page)
    print(f"Page generated successfully at {dest_path}")
    
if __name__ == "__main__":
    main()
