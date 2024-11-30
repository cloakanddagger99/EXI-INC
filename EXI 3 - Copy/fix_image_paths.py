import os
from bs4 import BeautifulSoup

# Base path to your website directory
website_dir = r"C:\Users\usama\OneDrive\Desktop\EXI 3 - Copy\exiinc.com"
old_path = "myrgroup.com"
new_path = "exiinc.com"

# Fix image paths in HTML/PHP files
def fix_image_paths(directory, old_path, new_path):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.html', '.php')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    modified = False
                    for img in soup.find_all('img'):
                        src = img.get('src')
                        if src and old_path in src:
                            img['src'] = src.replace(old_path, new_path)
                            modified = True
                    if modified:
                        with open(file_path, 'w', encoding='utf-8') as f_out:
                            f_out.write(str(soup))
                            print(f"Fixed paths in: {file_path}")

fix_image_paths(website_dir, old_path, new_path)
print("Image paths updated.")
