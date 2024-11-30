import os
from bs4 import BeautifulSoup

# Base directory of your website
base_dir = r"C:\Users\usama\OneDrive\Desktop\EXI 3 - Copy\exiinc.com"
# Image folder where your images are stored
image_base_folder = os.path.join(base_dir, "wp-content/uploads")

# Helper function to check if an image exists
def is_image_valid(image_path):
    return os.path.isfile(image_path)

# Function to fix broken image paths
def fix_image_paths():
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                html_file_path = os.path.join(root, file)
                with open(html_file_path, "r", encoding="utf-8") as html_file:
                    soup = BeautifulSoup(html_file, "html.parser")
                
                # Find all image tags in the HTML
                modified = False
                for img_tag in soup.find_all("img"):
                    img_src = img_tag.get("src")
                    if img_src:
                        # Get absolute path for the image
                        abs_image_path = os.path.abspath(os.path.join(root, img_src))
                        
                        # If the image is invalid, attempt to fix it
                        if not is_image_valid(abs_image_path):
                            # Attempt to find the correct path in the image folder
                            fixed_path = None
                            for subdir, _, images in os.walk(image_base_folder):
                                for image in images:
                                    if os.path.basename(img_src) == image:
                                        fixed_path = os.path.relpath(
                                            os.path.join(subdir, image), start=root
                                        ).replace("\\", "/")
                                        break
                                if fixed_path:
                                    break
                            
                            if fixed_path:
                                print(f"Fixing image: {img_src} -> {fixed_path}")
                                img_tag["src"] = fixed_path
                                modified = True
                            else:
                                print(f"Could not find a fix for image: {img_src}")

                # Save the fixed HTML file
                if modified:
                    with open(html_file_path, "w", encoding="utf-8") as html_file:
                        html_file.write(str(soup))
                        print(f"Updated file: {html_file_path}")

# Run the script
if __name__ == "__main__":
    fix_image_paths()
