import os
from bs4 import BeautifulSoup
import shutil

# Define the base directory
BASE_DIR = r"C:\Users\usama\OneDrive\Desktop\EXI 3 - Copy\exiinc.com"
IMAGE_BASE_PATH = os.path.join(BASE_DIR, "wp-content", "uploads")

# Log file for missing images
LOG_FILE = os.path.join(BASE_DIR, "fix_broken_image_paths.log")

# Placeholder for missing images
PLACEHOLDER_IMAGE = "/wp-content/uploads/placeholder.png"

# Helper: Find all image files in the project
def find_all_images(base_path):
    image_files = {}
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp')):
                relative_path = os.path.relpath(os.path.join(root, file), BASE_DIR)
                image_files[relative_path.replace("\\", "/")] = os.path.join(root, file)
    return image_files

# Helper: Write to the log file
def log_message(message):
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(message + "\n")

# Validate and fix image paths in HTML files
def validate_and_fix_image_paths(base_dir):
    all_images = find_all_images(IMAGE_BASE_PATH)
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")

                modified = False
                for img in soup.find_all("img"):
                    img_src = img.get("src", "").replace("../", "").replace("./", "").lstrip("/")
                    img_path = os.path.normpath(os.path.join(BASE_DIR, img_src))
                    
                    # Check if the image exists
                    if img_src not in all_images:
                        log_message(f"Missing image: {img_src} in file {file_path}")
                        print(f"Missing image: {img_src} in {file_path}")

                        # Attempt to auto-fix by finding similar images
                        suggestions = [key for key in all_images.keys() if os.path.basename(key) == os.path.basename(img_src)]
                        if suggestions:
                            best_match = suggestions[0]  # Choose the first match
                            img["src"] = "/" + best_match
                            modified = True
                            log_message(f"Auto-fixed {img_src} -> {best_match} in {file_path}")
                            print(f"Auto-fixed {img_src} -> {best_match} in {file_path}")
                        else:
                            # Replace with placeholder if no match is found
                            img["src"] = PLACEHOLDER_IMAGE
                            modified = True
                            log_message(f"Replaced {img_src} with placeholder in {file_path}")
                            print(f"Replaced {img_src} with placeholder in {file_path}")

                if modified:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(str(soup))

# Run the script
if __name__ == "__main__":
    # Clear log file
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    
    print("Validating and fixing image paths...")
    validate_and_fix_image_paths(BASE_DIR)
    print(f"Validation complete. See log: {LOG_FILE}")
