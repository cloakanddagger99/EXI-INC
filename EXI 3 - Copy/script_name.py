import os
import re

# Define root directory
root_directory = r"C:\Users\usama\OneDrive\Desktop\EXI 3 - Copy"

# Folder renaming
old_folder_name = "myrgroup.com"
new_folder_name = "exiinc.com"

# Step 1: Rename folder
old_path = os.path.join(root_directory, old_folder_name)
new_path = os.path.join(root_directory, new_folder_name)

try:
    os.rename(old_path, new_path)
    print(f"Renamed folder '{old_folder_name}' to '{new_folder_name}'")
except Exception as e:
    print(f"Error renaming folder: {e}")

# Step 2: Update all references in files
def update_references_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        updated_content = content.replace(old_folder_name, new_folder_name)

        if content != updated_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            print(f"Updated references in file: {file_path}")

    except Exception as e:
        print(f"Error updating file {file_path}: {e}")

# Step 3: Recursively update references in all files
def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(('.html', '.css', '.js', '.php', '.json')):
                update_references_in_file(file_path)

process_directory(root_directory)

# Step 4: Verify images
def verify_image_paths(directory):
    broken_links = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                file_path = os.path.join(root, file)
                if not os.path.exists(file_path):
                    broken_links.append(file_path)
    if broken_links:
        print("Broken image links found:")
        for link in broken_links:
            print(link)
    else:
        print("No broken image links found.")

verify_image_paths(new_path)
