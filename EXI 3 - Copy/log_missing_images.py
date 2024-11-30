import os
from bs4 import BeautifulSoup

# Base directory of the website
BASE_DIR = r"C:\Users\usama\OneDrive\Desktop\EXI 3 - Copy\exiinc.com"
LOG_FILE = os.path.join(BASE_DIR, "missing_images.log")

# Helper: Write log messages
def log_message(message):
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(message + "\n")

# Validate image paths
def validate_image_paths(base_dir):
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")

                for img in soup.find_all("img"):
                    img_src = img.get("src", "").strip()
                    if not img_src:
                        continue

                    img_path = os.path.join(base_dir, img_src.replace("/", os.sep))

                    # Check if the image file exists
                    if not os.path.exists(img_path):
                        log_message(f"Missing image: {img_src} in {file_path}")
                        print(f"Missing image: {img_src} in {file_path}")

# Run the script
if __name__ == "__main__":
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)  # Clear previous log
    print("Validating image paths...")
    validate_image_paths(BASE_DIR)
    print(f"Validation complete. Check log: {LOG_FILE}")
