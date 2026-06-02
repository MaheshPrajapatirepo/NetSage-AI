import os

project_name = "Main_Folder"

folders = [
    "data/raw_logs",
    "data/processed",
    "data/datasets",
    "models",
    "outputs",
    "visuals",
    "notebooks",
    "src"
]

files = {

    "app.py": "",

    "main.py": "",

    "README.md": "# NetSage AI\n",

    ".gitignore": """\
__pycache__/
.ipynb_checkpoints/
*.pyc
.env
""",

    "requirements.txt": """\
pandas
numpy
matplotlib
scikit-learn
streamlit
joblib
""",

    "src/log_collector.py": "",

    "src/log_parser.py": "",

    "src/feature_engineering.py": "",

    "src/train.py": "",

    "src/evaluate.py": "",

    "src/inference.py": "",

    "data/raw_logs/sample_syslog.log": ""
}

def create_structure():
    print(f"\n📁 Creating project: {project_name}\n")

    # ── Create Folders ────────────────────────────────────────────
    for folder in folders:
        folder_path = os.path.join(project_name, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"  ✅ Created folder  : {folder_path}")
        else:
            print(f"  ⚠️  Already exists  : {folder_path}")

    # ── Create src folder separately ──────────────────────────────
    src_path = os.path.join(project_name, "src")
    if not os.path.exists(src_path):
        os.makedirs(src_path)
        print(f"  ✅ Created folder  : {src_path}")

    print()

    # ── Create Files ──────────────────────────────────────────────
    for file, content in files.items():
        file_path = os.path.join(project_name, file)

        # ensure parent folder exists
        parent = os.path.dirname(file_path)
        if not os.path.exists(parent):
            os.makedirs(parent)

        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(content)
            print(f"  ✅ Created file    : {file_path}")
        else:
            print(f"  ⚠️  Already exists  : {file_path}")

    print(f"""
{'='*45}
✅ Project structure created successfully!

📁 {project_name}/
   ├── app.py
   ├── main.py
   ├── requirements.txt
   ├── README.md
   ├── .gitignore
   ├── src/
   │   ├── data_generator.py
   │   ├── data_loader.py
   │   ├── train.py
   │   ├── evaluate.py
   │   └── export_model.py
   ├── data/
   ├── models/
   ├── outputs/
   └── visuals/

Next steps:
  1. Copy your src/ files into {project_name}/src/
  2. Run: python {project_name}/main.py
  3. Run: streamlit run {project_name}/app.py
{'='*45}
""")

if __name__ == "__main__":
    create_structure()