import os

# Define the base directory
base_dir = r"C:\Users\usama\OneDrive\Desktop\EXI 3 - Copy"

# Original and new folder names
old_folder = "myrgroup.com"
new_folder = "exiinc.com"

# Path for the original and new folders
old_path = os.path.join(base_dir, old_folder)
new_path = os.path.join(base_dir, new_folder)

# Rename folder
try:
    os.rename(old_path, new_path)
    print(f"Folder renamed from {old_folder} to {new_folder}")
except FileNotFoundError:
    print(f"Error: The folder {old_folder} does not exist.")
    exit()
except Exception as e:
    print(f"Error renaming folder: {e}")
    exit()

# Traverse all files in the new directory
for root, _, files in os.walk(new_path):
    for file in files:
        file_path = os.path.join(root, file)

        # Replace content in files
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Replace all instances of the old folder name with the new one
            updated_content = content.replace(old_folder, new_folder)

            # Write back to the file if changes were made
            if content != updated_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                print(f"Updated references in: {file_path}")

        except UnicodeDecodeError:
            # Skip binary files like images, videos, etc.
            print(f"Skipped binary file: {file_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

print("All references updated successfully.")
