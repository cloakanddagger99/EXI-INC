import os
from bs4 import BeautifulSoup

# Set the directory to scan
website_dir = r"C:\Users\usama\OneDrive\Desktop\EXI 3 - Copy\exiinc.com"

# Path to the folder containing images
image_folder = os.path.join(website_dir, "wp-content")

# Scan HTML files and check image references
def find_broken_images(directory):
    broken_images = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.html', '.php')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    for img in soup.find_all('img'):
                        src = img.get('src')
                        if src and not src.startswith(('http://', 'https://')):
                            # Convert relative path to absolute path
                            image_path = os.path.normpath(os.path.join(root, src))
                            if not os.path.exists(image_path):
                                broken_images.append((file_path, src))
    return broken_images

# Find and display broken images
broken = find_broken_images(website_dir)
if broken:
    print("Broken image references found:")
    for file_path, src in broken:
        print(f"In file: {file_path}, missing image: {src}")
else:
    print("No broken image references found.")
