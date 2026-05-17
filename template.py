import os

project_name = "Main_Folder"

folders = [
    "data",
    "models",
    "outputs",
    "visuals",
    "src"
]

files = {
    "requirements.txt": """\
pandas
numpy
matplotlib
seaborn
scikit-learn
streamlit
joblib
""",

    "README.md": """\
# 📡 NetSage AI

An AI-powered Network Operations Center (NOC) monitoring and incident prediction system built with Python, scikit-learn, and Streamlit.

## 🚀 How to Run

### Step 1 — Run full pipeline
```bash
python main.py
```

### Step 2 — Launch Streamlit app
```bash
streamlit run app.py
```
""",

    ".gitignore": """\
# Python
__pycache__/
*.py[cod]
*.pyo
.Python

# Virtual Environments
venv/
env/
.env
.venv

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Models
models/*.pkl

# macOS
.DS_Store

# VSCode
.vscode/

# Logs
*.log
""",

    "main.py": "# main.py — Run this to execute full pipeline\n",
    "app.py" : "# app.py  — Run this to launch Streamlit dashboard\n",

    "src/__init__.py"       : "",
    "src/data_generator.py" : "# src/data_generator.py — Generate synthetic network data\n",
    "src/data_loader.py"    : "# src/data_loader.py    — Load, encode and prepare features\n",
    "src/train.py"          : "# src/train.py          — Cross validation + train model\n",
    "src/evaluate.py"       : "# src/evaluate.py       — Metrics, confusion matrix, feature importance\n",
    "src/export_model.py"   : "# src/export_model.py   — Save and load .pkl files\n",

    "data/.gitkeep"    : "",
    "models/.gitkeep"  : "",
    "outputs/.gitkeep" : "",
    "visuals/.gitkeep" : "",
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