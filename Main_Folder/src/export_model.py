import joblib
import os

MODELS_DIR = "models"

def save_model(obj, filename):
    os.makedirs(MODELS_DIR, exist_ok=True)
    path = os.path.join(MODELS_DIR, filename)
    joblib.dump(obj, path)
    print(f"✅ Saved → {path}")

def load_model(filename):
    path = os.path.join(MODELS_DIR, filename)
    obj = joblib.load(path)
    print(f"✅ Loaded ← {path}")
    return obj