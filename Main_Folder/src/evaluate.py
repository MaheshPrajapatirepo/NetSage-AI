import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, roc_auc_score
)

def evaluate_model(model, X_test, Y_test, model_name, scaler=None):
    if scaler is not None:
        X_test = scaler.transform(X_test)

    preds   = model.predict(X_test)
    proba   = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(Y_test, preds) * 100
    roc_auc  = roc_auc_score(Y_test, proba)  * 100

    print(f"\n{'='*45}")
    print(f"  {model_name}")
    print(f"{'='*45}")
    print(f"  Accuracy : {accuracy:.2f}%")
    print(f"  ROC-AUC  : {roc_auc:.2f}%")
    print(f"\n{classification_report(Y_test, preds, target_names=['Non-Critical', 'Critical'])}")

    return {'Model': model_name, 'Accuracy': accuracy, 'ROC_AUC': roc_auc}

def plot_confusion_matrix(model, X_test, Y_test, scaler=None):
    if scaler is not None:
        X_test = scaler.transform(X_test)

    preds = model.predict(X_test)
    cm    = confusion_matrix(Y_test, preds)

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Purples',
        xticklabels=['Non-Critical', 'Critical'],
        yticklabels=['Non-Critical', 'Critical'],
        ax=ax
    )
    ax.set_title('Confusion Matrix — Random Forest', fontweight='bold')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    plt.tight_layout()
    os.makedirs("outputs", exist_ok=True)
    plt.savefig('outputs/confusion_matrix.png', bbox_inches='tight')
    plt.show()
    plt.close()

def plot_feature_importance(model, feature_names):
    fi = pd.DataFrame({
        'Feature'   : feature_names,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=fi, x='Importance', y='Feature', ax=ax)
    ax.set_title('Feature Importance — Random Forest', fontweight='bold')
    plt.tight_layout()
    os.makedirs("outputs", exist_ok=True)
    plt.savefig('outputs/feature_importance.png', bbox_inches='tight')
    plt.show()
    plt.close()

    print("\nFeature Importance:")
    print(fi.to_string(index=False))
    return fi