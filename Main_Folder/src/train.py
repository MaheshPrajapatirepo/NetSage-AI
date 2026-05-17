import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# ── Scoring ───────────────────────────────────────────────────────
SCORING = {
    'accuracy': 'accuracy',
    'f1'      : 'f1',
    'roc_auc' : 'roc_auc'
}

# ── Models ────────────────────────────────────────────────────────
# max_depth and min_samples_leaf are set to prevent overfitting
MODELS = {
    'LogisticRegression'    : LogisticRegression(random_state=42, max_iter=1000),
    'DecisionTreeClassifier': DecisionTreeClassifier(
                                random_state=42,
                                max_depth=5,           # prevents overfit
                                min_samples_leaf=10    # prevents overfit
                              ),
    'RandomForestClassifier': RandomForestClassifier(
                                random_state=42,
                                n_estimators=100,
                                max_depth=8,           # prevents overfit
                                min_samples_leaf=5,    # prevents overfit
                                max_features='sqrt'    # prevents overfit
                              ),
}

def run_cross_validation(X_train, Y_train, cv=5):
    results = []
    for name, model in MODELS.items():
        pipe = Pipeline(steps=[
            ('scaler', StandardScaler()),
            ('model',  model)
        ])
        cv_results = cross_validate(pipe, X_train, Y_train, cv=cv, scoring=SCORING)
        results.append({
            'Model'      : name,
            'CV Accuracy': cv_results['test_accuracy'].mean().round(4),
            'CV F1'      : cv_results['test_f1'].mean().round(4),
            'CV ROC-AUC' : cv_results['test_roc_auc'].mean().round(4),
        })
    df = pd.DataFrame(results).sort_values(by='CV ROC-AUC', ascending=False).reset_index(drop=True)
    print("\n=== Cross-Validation Results ===")
    print(df.to_string(index=False))
    return df

def train_best_model(X_train, Y_train):
    # Best model with anti-overfit params applied directly
    model = RandomForestClassifier(
        n_estimators    = 100,
        max_depth       = 8,
        min_samples_leaf= 5,
        min_samples_split= 10,
        max_features    = 'sqrt',
        random_state    = 42
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    model.fit(X_train_scaled, Y_train)
    print("\n✅ Best model trained — Random Forest (anti-overfit params)")
    return model, scaler