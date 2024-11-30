import os
from bs4 import BeautifulSoup
import difflib

# Define your base directory and assets directory
base_dir = r"C:\Users\usama\OneDrive\Desktop\EXI 3 - Copy\exiinc.com"
assets_dir = os.path.join(base_dir, "wp-content", "uploads")
log_file = "fix_broken_image_paths.log"

def find_similar_images(image_name, search_dir):
    """Find similar image names in the given directory."""
    matches = []
    for root, _, files in os.walk(search_dir):
        for file in files:
            if difflib.SequenceMatcher(None, image_name, file).ratio() > 0.6:
                matches.append(os.path.join(root, file))
    return matches

def fix_image_paths():
    """Find and attempt to fix broken image paths."""
    unresolved_images = []
    with open(log_file, "w", encoding="utf-8") as log:
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".html"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as html_file:
                        soup = BeautifulSoup(html_file, "html.parser")
                    modified = False

                    # Process <img> tags
                    for img_tag in soup.find_all("img"):
                        src = img_tag.get("src")
                        if src:
                            full_path = os.path.normpath(os.path.join(root, src))
                            if not os.path.exists(full_path):
                                unresolved_images.append((file_path, src))
                                log.write(f"Missing image: {src} in file {file_path}\n")
                                # Attempt to find similar images
                                image_name = os.path.basename(src)
                                similar_images = find_similar_images(image_name, assets_dir)
                                if similar_images:
                                    log.write(f"Suggested matches for {src}:\n")
                                    for match in similar_images:
                                        log.write(f"  - {match}\n")
                                    # Replace with the first match (or provide manual fix)
                                    new_src = os.path.relpath(similar_images[0], root).replace("\\", "/")
                                    img_tag["src"] = new_src
                                    modified = True
                                else:
                                    log.write(f"No suggestions found for {src}\n")

                    # Save modifications if any
                    if modified:
                        with open(file_path, "w", encoding="utf-8") as html_file:
                            html_file.write(str(soup))

    # Log unresolved images
    print("Unresolved images and potential fixes logged to:", log_file)
    if unresolved_images:
        print("Unresolved images found:")
        for file_path, src in unresolved_images:
            print(f"  Missing {src} in {file_path}")

if __name__ == "__main__":
    fix_image_paths()
