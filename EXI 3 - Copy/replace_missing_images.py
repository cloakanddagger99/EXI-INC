import os
from bs4 import BeautifulSoup

# Define placeholder image
PLACEHOLDER_IMAGE = "../../wp-content/uploads/2022/04/placeholder.png"
BASE_DIR = r"C:\Users\usama\OneDrive\Desktop\EXI 3 - Copy"

def replace_missing_images(base_dir):
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                
                modified = False
                for img in soup.find_all('img'):
                    img_src = img.get('src', '')
                    img_path = os.path.normpath(os.path.join(root, img_src))
                    if not os.path.exists(img_path):
                        print(f"Replacing missing image: {img_src} in file {file_path}")
                        img['src'] = PLACEHOLDER_IMAGE
                        modified = True
                
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(str(soup))

replace_missing_images(BASE_DIR)
