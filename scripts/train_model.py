"""Train late-delivery risk models.

This script trains an operational prediction model that deliberately excludes
post-shipment leakage fields such as actual shipping days and delivery status.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "orders_clean.csv"
MARTS = ROOT / "data" / "marts"
MODELS = ROOT / "models"

TARGET = "late_delivery_risk"
LEAKAGE_COLUMNS = {
    TARGET,
    "is_late",
    "delivery_status",
    "days_for_shipping_real",
    "shipping_gap",
    "shipping_date_dateorders",
    "order_status",
    "order_profit_per_order",  # duplicated outcome-like financial field
}

NUMERIC_FEATURES = [
    "days_for_shipment_scheduled",
    "sales_per_customer",
    "order_item_discount",
    "order_item_discount_rate",
    "order_item_product_price",
    "order_item_quantity",
    "sales",
    "order_item_total",
    "product_price",
    "order_year",
]

CATEGORICAL_FEATURES = [
    "type",
    "category_name",
    "customer_city",
    "customer_country",
    "customer_segment",
    "customer_state",
    "department_name",
    "market",
    "order_country",
    "order_region",
    "order_state",
    "shipping_mode",
    "order_quarter",
    "order_dayofweek",
]


def make_preprocessor(num_cols: list[str], cat_cols: list[str]) -> ColumnTransformer:
    numeric = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", min_frequency=50)),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("num", numeric, num_cols),
            ("cat", categorical, cat_cols),
        ]
    )


def evaluate_model(model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]
    cm = confusion_matrix(y_test, pred).tolist()
    return {
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision_late": float(precision_score(y_test, pred, zero_division=0)),
        "recall_late": float(recall_score(y_test, pred, zero_division=0)),
        "f1_late": float(f1_score(y_test, pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, prob)),
        "confusion_matrix": cm,
    }


def feature_importance(model: Pipeline, num_cols: list[str], cat_cols: list[str], top_n: int = 40) -> pd.DataFrame:
    pre = model.named_steps["preprocessor"]
    clf = model.named_steps["classifier"]
    try:
        cat_names = pre.named_transformers_["cat"].named_steps["onehot"].get_feature_names_out(cat_cols).tolist()
        names = num_cols + cat_names
    except Exception:
        names = num_cols + cat_cols

    if hasattr(clf, "feature_importances_"):
        values = clf.feature_importances_
        importance_type = "gini_importance"
    elif hasattr(clf, "coef_"):
        values = np.abs(clf.coef_[0])
        importance_type = "absolute_coefficient"
    else:
        values = np.zeros(len(names))
        importance_type = "unknown"

    n = min(len(names), len(values))
    out = pd.DataFrame({"feature": names[:n], "importance": values[:n]})
    out["importance_type"] = importance_type
    return out.sort_values("importance", ascending=False).head(top_n)


def risk_level(prob: float) -> str:
    if prob < 0.40:
        return "Low"
    if prob < 0.70:
        return "Medium"
    return "High"


def main() -> None:
    MARTS.mkdir(parents=True, exist_ok=True)
    MODELS.mkdir(parents=True, exist_ok=True)

    print(f"Reading {DATA}")
    df = pd.read_csv(DATA, low_memory=False)
    y = df[TARGET].astype(int)

    num_cols = [c for c in NUMERIC_FEATURES if c in df.columns and c not in LEAKAGE_COLUMNS]
    cat_cols = [c for c in CATEGORICAL_FEATURES if c in df.columns and c not in LEAKAGE_COLUMNS]
    X = df[num_cols + cat_cols].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    preprocessor = make_preprocessor(num_cols, cat_cols)
    candidates = {
        "logistic_regression": Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                (
                    "classifier",
                    LogisticRegression(max_iter=700, class_weight="balanced", n_jobs=-1),
                ),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                ("preprocessor", make_preprocessor(num_cols, cat_cols)),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=120,
                        max_depth=16,
                        min_samples_leaf=25,
                        class_weight="balanced_subsample",
                        random_state=42,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
    }

    metrics: dict[str, dict] = {}
    best_name = None
    best_score = -1.0
    for name, model in candidates.items():
        print(f"Training {name}")
        model.fit(X_train, y_train)
        m = evaluate_model(model, X_test, y_test)
        metrics[name] = m
        # Business priority: recall first, then F1 and AUC.
        composite = (m["recall_late"] * 0.50) + (m["f1_late"] * 0.30) + (m["roc_auc"] * 0.20)
        print(name, json.dumps(m, indent=2))
        if composite > best_score:
            best_score = composite
            best_name = name

    assert best_name is not None
    best_model = candidates[best_name]
    joblib.dump(best_model, MODELS / "late_delivery_risk_model.joblib")

    metrics_out = {
        "target": TARGET,
        "business_priority": "Recall for late-delivery class is prioritized because missing risky shipments is costlier than over-flagging.",
        "model_type": "operational_prediction_no_post_shipment_leakage",
        "excluded_leakage_columns": sorted(LEAKAGE_COLUMNS),
        "features_used": {"numeric": num_cols, "categorical": cat_cols},
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "best_model": best_name,
        "metrics": metrics,
    }
    with open(MARTS / "model_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics_out, f, indent=2)

    feature_importance(best_model, num_cols, cat_cols).to_csv(MARTS / "feature_importance.csv", index=False)

    # Scoring sample for dashboard: deterministic sample from test set.
    sample = X_test.sample(n=min(500, len(X_test)), random_state=7).copy()
    prob = best_model.predict_proba(sample)[:, 1]
    scored = df.loc[sample.index, [
        "order_id",
        "shipping_mode",
        "market",
        "order_region",
        "order_country",
        "category_name",
        "customer_segment",
        "sales",
        TARGET,
    ]].copy()
    scored["delivery_risk_probability"] = prob
    scored["risk_level"] = scored["delivery_risk_probability"].map(risk_level)
    scored.sort_values("delivery_risk_probability", ascending=False).to_csv(
        MARTS / "model_scoring_sample.csv", index=False
    )

    print(f"Best model: {best_name}")
    print(f"Wrote metrics/model artifacts to {MARTS} and {MODELS}")


if __name__ == "__main__":
    main()
