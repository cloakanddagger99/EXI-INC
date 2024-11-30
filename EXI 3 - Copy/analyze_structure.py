import os
from bs4 import BeautifulSoup

# Directory to analyze
root_dir = r"C:\Users\usama\OneDrive\Desktop\EXI 3 - Copy"

# Function to extract links from HTML/PHP files
def extract_links_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            links = []
            # Extract 'href' and 'src' attributes
            for tag in soup.find_all(['a', 'img', 'link', 'script']):
                link = tag.get('href') or tag.get('src')
                if link:
                    links.append(link)
            return links
    except Exception as e:
        return [f"Error reading {file_path}: {str(e)}"]

# Walk the directory and gather data
structure = []
for root, dirs, files in os.walk(root_dir):
    structure.append({"Directory": root, "Subdirectories": dirs, "Files": files})
    for file in files:
        if file.endswith(('.html', '.php')):
            file_path = os.path.join(root, file)
            links = extract_links_from_file(file_path)
            structure.append({"HTML/PHP File": file_path, "Links": links})
        elif file.endswith(('.jpg', '.png', '.gif', '.svg')):
            structure.append({"Image File": os.path.join(root, file)})

# Save or display the structure
output_file = os.path.join(root_dir, "website_structure.txt")
with open(output_file, "w", encoding="utf-8") as f:
    for item in structure:
        f.write(str(item) + "\n")

print(f"Website structure saved to {output_file}")
