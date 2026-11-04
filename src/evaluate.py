import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score


def evaluate(y_true, y_pred, name):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    print(f"--- {name} ---")
    print(f"Precision: {precision_score(y_true, y_pred, zero_division=0):.4f}")
    print(f"Recall:    {recall_score(y_true, y_pred, zero_division=0):.4f}")
    print(f"F1:        {f1_score(y_true, y_pred, zero_division=0):.4f}")
    print(f"Missed attacks (FN): {fn}   False alarms (FP): {fp}\n")


def recall_by_attack(label_test, y_pred):
    df = pd.DataFrame({"label": label_test.values, "flagged": y_pred})
    attacks = df[df["label"] != "BENIGN"]
    return attacks.groupby("label")["flagged"].mean().sort_values()