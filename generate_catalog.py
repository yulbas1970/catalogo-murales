import os
import re
import requests # Import requests library

def generate_catalog(base_path):
    # Fetch image URLs from the Node.js backend
    backend_api_url = "http://localhost:5000/api/mobile-catalog-images"
    try:
        response = requests.get(backend_api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        image_files = response.json()
        print(f"DEBUG: Fetched {len(image_files)} image URLs from backend: {image_files}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image URLs from backend: {e}")
        print("Falling back to local file scan.")
        # Fallback to local file scan if backend is not available
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif')
        image_files = []
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.lower().endswith(image_extensions):
                    relative_path = os.path.relpath(os.path.join(root, file), base_path)
                    image_files.append(relative_path.replace('\\', '/'))


    # Read the existing HTML content
    html_file_path = os.path.join(base_path, 'catalogo.html')
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Generate the new JavaScript array string
    js_array_items = [f"'{f}'" for f in image_files]
    new_js_array = f"const imageFiles = [\n{',\\n'.join(js_array_items)}\n];"
    print(f"DEBUG: Generated new_js_array:\n{new_js_array}")

    # Find the old imageFiles array and replace it
    pattern = re.compile(r"const imageFiles = \[\s*[\s\S]*?\];", re.MULTILINE)
    
    # Check if a substitution actually happens
    updated_html_content, num_substitutions = pattern.subn(new_js_array, html_content)
    print(f"DEBUG: Number of substitutions made: {num_substitutions}")

    if num_substitutions > 0:
        # Write the updated HTML content back to the file
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_html_content)
        print(f"Catalog updated successfully with {len(image_files)} images.")
    else:
        print("DEBUG: No changes detected in imageFiles array, catalogo.html not modified.")
        print(f"Catalog is already up to date with {len(image_files)} images.")


if __name__ == "__main__":
    # The script assumes it's run from the CATALOGO_MURALES directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    generate_catalog(script_dir)