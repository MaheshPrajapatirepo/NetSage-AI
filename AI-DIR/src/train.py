import pandas as pd
import os
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

# this module trains a simple classifier to predict risk level
# from the engineered features — useful for pattern detection
# and failure prediction in phase 2 of the roadmap

MODEL_META_PATH = "AI-DIR/data/processed/model_meta.json"


def load_features(input_path="AI-DIR/data/processed/feature_logs.csv"):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"feature logs not found: {input_path}")

    df = pd.read_csv(input_path, parse_dates=["timestamp"])
    return df


def prepare_data(df):
    # features the model will learn from
    feature_cols = ["severity_score", "protocol_risk", "state_risk", "event_count_10m"]
    target_col   = "risk_level"

    # drop rows with missing values in feature columns
    df = df.dropna(subset=feature_cols + [target_col])

    X = df[feature_cols]
    y = df[target_col]

    # encode labels: CRITICAL, HIGH, MEDIUM, LOW → integers
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    return X, y_encoded, le, feature_cols


def train(input_path="AI-DIR/data/processed/feature_logs.csv"):
    print("loading features...")
    df = load_features(input_path)

    print("preparing data...")
    X, y, le, feature_cols = prepare_data(df)

    if len(X) < 10:
        raise ValueError("not enough data to train — run collector.py first to generate more logs")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"training on {len(X_train)} samples, testing on {len(X_test)} samples...")

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42,
        class_weight="balanced"  # handles imbalanced risk levels
    )
    model.fit(X_train, y_train)

    # evaluate
    y_pred = model.predict(X_test)
    labels = le.inverse_transform(sorted(set(y_test)))

    print("\n--- evaluation ---")
    print(classification_report(y_test, y_pred, target_names=labels))

    print("confusion matrix:")
    cm = confusion_matrix(y_test, y_pred)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    print(cm_df.to_string())

    # feature importance
    print("\nfeature importance:")
    for feat, score in sorted(
        zip(feature_cols, model.feature_importances_),
        key=lambda x: x[1], reverse=True
    ):
        print(f"  {feat:<20} {score:.4f}")

    # save model metadata so inference can reference it later
    meta = {
        "features":    feature_cols,
        "classes":     list(le.classes_),
        "n_estimators": model.n_estimators,
        "train_size":  len(X_train),
        "test_size":   len(X_test),
    }
    with open(MODEL_META_PATH, "w") as f:
        json.dump(meta, f, indent=2)

    print(f"\nmodel meta saved → {MODEL_META_PATH}")
    return model, le


if __name__ == "__main__":
    train()