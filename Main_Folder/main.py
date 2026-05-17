"""
main.py — NetSage AI Pipeline
Run: python main.py
Generates data → trains model → saves model + scaler
"""

from sklearn.model_selection import train_test_split

from src.data_generator import generate_data
from src.data_loader    import create_target, encode_features, get_features_and_target
from src.train          import run_cross_validation, train_best_model
from src.evaluate       import evaluate_model, plot_confusion_matrix, plot_feature_importance
from src.export_model   import save_model

import os

def main():

    # ── 1. Generate / Load Data ──────────────────────────────────
    print("📡 Generating network incident data...")
    os.makedirs("data", exist_ok=True)
    df = generate_data(n=1000)
    df.to_csv("data/network_incidents.csv", index=False)
    print(f"✅ {len(df)} rows generated")
    print(f"\nSeverity distribution:\n{df['Severity'].value_counts()}")

    # ── 2. Prepare Features ──────────────────────────────────────
    print("\n⚙️  Preparing features...")
    df = create_target(df)
    df, categories = encode_features(df)
    X, y = get_features_and_target(df)

    print(f"\nTarget distribution:\n{y.value_counts()}")

    # ── 3. Train Test Split ──────────────────────────────────────
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ── 4. Cross Validation ──────────────────────────────────────
    print("\n🔁 Running Cross Validation...")
    run_cross_validation(X_train, Y_train)

    # ── 5. Train Best Model ──────────────────────────────────────
    print("\n🚀 Training best model...")
    model, scaler = train_best_model(X_train, Y_train)

    # ── 6. Evaluate ──────────────────────────────────────────────
    print("\n📊 Evaluating...")
    evaluate_model(model, X_test, Y_test, 'Random Forest', scaler)
    plot_confusion_matrix(model, X_test, Y_test, scaler)
    plot_feature_importance(model, X_train.columns)

    # ── 7. Save ──────────────────────────────────────────────────
    print("\n💾 Saving model and scaler...")
    save_model(model,      "netsage_model.pkl")
    save_model(scaler,     "netsage_scaler.pkl")
    save_model(categories, "netsage_categories.pkl")

    print("\n✅ Pipeline complete!")
    print("Run: streamlit run app.py")

if __name__ == "__main__":
    main()