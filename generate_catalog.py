import os
import re

def generate_catalog(base_path):
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif')
    image_files = []

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(image_extensions):
                relative_path = os.path.relpath(os.path.join(root, file), base_path)
                # Replace backslashes with forward slashes for web paths
                image_files.append(relative_path.replace('\\', '/'))

    # Read the existing HTML content
    html_file_path = os.path.join(base_path, 'catalogo.html')
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Generate the new JavaScript array string
    js_array_items = [f"'{f}'" for f in image_files]
    new_js_array = f"const imageFiles = [\n{',\\n'.join(js_array_items)}\n];"

    # Find the old imageFiles array and replace it
    # This regex looks for 'const imageFiles = [' followed by any content until '];'
    # It's important to be specific enough to avoid replacing other JS code
    pattern = re.compile(r"const imageFiles = \[\n(?:.|\n)*?\];", re.MULTILINE)
    updated_html_content = pattern.sub(new_js_array, html_content)

    # Write the updated HTML content back to the file
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(updated_html_content)

    print(f"Catalog updated successfully with {len(image_files)} images.")

if __name__ == "__main__":
    # The script assumes it's run from the CATALOGO_MURALES directory
    # or that base_path is correctly set.
    # For this context, base_path is the current directory where the script resides.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    generate_catalog(script_dir)