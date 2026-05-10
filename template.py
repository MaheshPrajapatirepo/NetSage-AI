import os

project_name = "NetSage-AI"

folders = [
    "data",
    "notebooks",
    "scripts",
    "visuals",
    "models",
    "reports"
]

files = [
    "README.md",
    "requirements.txt",
    "main.py",
    ".gitignore",
    "setup.py"
]

# Create folders
for folder in folders:
    folder_path = os.path.join(project_name, folder)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

    else:
        print(f"Folder already exists: {folder_path}")

# Create files
for file in files:
    file_path = os.path.join(project_name, file)

    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            pass

        print(f"Created file: {file_path}")

    else:
        print(f"File already exists: {file_path}")

print("\nProject structure setup completed.")