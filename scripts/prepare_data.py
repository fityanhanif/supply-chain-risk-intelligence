"""Prepare clean supply chain data and KPI marts.

Input:
    data/raw/DataCoSupplyChainDataset.csv

Outputs:
    data/processed/orders_clean.csv
    data/marts/delivery_kpis.csv
    data/marts/profitability_kpis.csv
    data/marts/region_shipping_kpis.csv
    data/marts/category_performance.csv
    data/marts/monthly_delivery_trend.csv
    data/marts/data_profile.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "DataCoSupplyChainDataset.csv"
PROCESSED = ROOT / "data" / "processed"
MARTS = ROOT / "data" / "marts"

PII_COLUMNS = {
    "customer_email",
    "customer_fname",
    "customer_lname",
    "customer_password",
    "customer_street",
    "customer_zipcode",
    "latitude",
    "longitude",
    "product_image",
    "product_description",
}


def clean_col(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    # Normalize the dataset's inconsistent wording.
    name = name.replace("days_for_shipment_scheduled", "days_for_shipment_scheduled")
    return name


def safe_divide(num: pd.Series, den: pd.Series) -> pd.Series:
    den = den.replace({0: np.nan})
    return (num / den).replace([np.inf, -np.inf], np.nan)


def late_rate(x: pd.Series) -> float:
    return float(x.mean()) if len(x) else 0.0


def summarize_group(df: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    out = (
        df.groupby(by, dropna=False)
        .agg(
            orders=("order_id", "nunique"),
            late_orders=("late_delivery_risk", "sum"),
            late_rate=("late_delivery_risk", "mean"),
            sales=("sales", "sum"),
            profit=("benefit_per_order", "sum"),
            avg_shipping_days=("days_for_shipping_real", "mean"),
            avg_scheduled_days=("days_for_shipment_scheduled", "mean"),
            avg_shipping_gap=("shipping_gap", "mean"),
        )
        .reset_index()
    )
    out["profit_margin"] = safe_divide(out["profit"], out["sales"])
    return out.sort_values(["orders", "late_rate"], ascending=[False, False])


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    MARTS.mkdir(parents=True, exist_ok=True)

    print(f"Reading {RAW}")
    df = pd.read_csv(RAW, encoding="cp1252", low_memory=False)
    original_shape = df.shape
    df.columns = [clean_col(c) for c in df.columns]

    # Remove direct PII / fields not useful for portfolio analytics.
    df = df.drop(columns=[c for c in PII_COLUMNS if c in df.columns], errors="ignore")

    # Parse dates.
    for c in ["order_date_dateorders", "shipping_date_dateorders"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    # Numeric coercion for expected numeric fields.
    numeric_cols = [
        "days_for_shipping_real",
        "days_for_shipment_scheduled",
        "benefit_per_order",
        "sales_per_customer",
        "late_delivery_risk",
        "order_item_discount",
        "order_item_discount_rate",
        "order_item_product_price",
        "order_item_profit_ratio",
        "order_item_quantity",
        "sales",
        "order_item_total",
        "order_profit_per_order",
        "product_price",
    ]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Feature engineering.
    df["shipping_gap"] = df["days_for_shipping_real"] - df["days_for_shipment_scheduled"]
    df["is_late"] = df["late_delivery_risk"].astype("Int64")
    df["is_loss_making"] = (df["benefit_per_order"] < 0).astype(int)
    df["profit_margin"] = safe_divide(df["benefit_per_order"], df["sales"])
    df["profit_margin"] = df["profit_margin"].clip(-2, 2)

    if "order_date_dateorders" in df.columns:
        df["order_year"] = df["order_date_dateorders"].dt.year
        df["order_month"] = df["order_date_dateorders"].dt.to_period("M").astype(str)
        df["order_quarter"] = df["order_date_dateorders"].dt.to_period("Q").astype(str)
        df["order_dayofweek"] = df["order_date_dateorders"].dt.day_name()

    # Keep an anonymized clean dataset. Limit text object whitespace.
    obj_cols = df.select_dtypes(include="object").columns
    for c in obj_cols:
        df[c] = df[c].astype(str).str.strip().replace({"nan": np.nan, "None": np.nan})

    clean_path = PROCESSED / "orders_clean.csv"
    df.to_csv(clean_path, index=False)
    print(f"Wrote {clean_path} rows={len(df):,} cols={len(df.columns):,}")

    # Marts.
    delivery_dims = ["shipping_mode", "market", "order_region", "category_name", "customer_segment"]
    summarize_group(df, ["shipping_mode"]).to_csv(MARTS / "delivery_kpis.csv", index=False)
    summarize_group(df, ["market", "order_region", "shipping_mode"]).to_csv(MARTS / "region_shipping_kpis.csv", index=False)
    summarize_group(df, ["category_name", "department_name"]).to_csv(MARTS / "category_performance.csv", index=False)
    summarize_group(df, ["customer_segment", "market"]).to_csv(MARTS / "customer_market_kpis.csv", index=False)

    profitability = (
        df.groupby(["market", "order_region", "category_name"], dropna=False)
        .agg(
            orders=("order_id", "nunique"),
            sales=("sales", "sum"),
            profit=("benefit_per_order", "sum"),
            avg_discount_rate=("order_item_discount_rate", "mean"),
            loss_orders=("is_loss_making", "sum"),
            late_rate=("late_delivery_risk", "mean"),
        )
        .reset_index()
    )
    profitability["profit_margin"] = safe_divide(profitability["profit"], profitability["sales"])
    profitability["loss_order_rate"] = safe_divide(profitability["loss_orders"], profitability["orders"])
    profitability.sort_values("sales", ascending=False).to_csv(MARTS / "profitability_kpis.csv", index=False)

    monthly = (
        df.groupby("order_month", dropna=False)
        .agg(
            orders=("order_id", "nunique"),
            late_orders=("late_delivery_risk", "sum"),
            late_rate=("late_delivery_risk", "mean"),
            sales=("sales", "sum"),
            profit=("benefit_per_order", "sum"),
            avg_shipping_gap=("shipping_gap", "mean"),
        )
        .reset_index()
        .sort_values("order_month")
    )
    monthly.to_csv(MARTS / "monthly_delivery_trend.csv", index=False)

    profile = {
        "source_file": str(RAW),
        "original_rows": int(original_shape[0]),
        "original_columns": int(original_shape[1]),
        "clean_rows": int(df.shape[0]),
        "clean_columns": int(df.shape[1]),
        "late_delivery_orders": int(df["late_delivery_risk"].sum()),
        "late_delivery_rate": float(df["late_delivery_risk"].mean()),
        "total_sales": float(df["sales"].sum()),
        "total_profit": float(df["benefit_per_order"].sum()),
        "avg_profit_margin": float(safe_divide(df["benefit_per_order"], df["sales"]).mean()),
        "delivery_status": df["delivery_status"].value_counts(dropna=False).to_dict(),
        "shipping_mode": df["shipping_mode"].value_counts(dropna=False).to_dict(),
        "market": df["market"].value_counts(dropna=False).to_dict(),
        "removed_pii_columns": sorted([c for c in PII_COLUMNS if c in [clean_col(x) for x in pd.read_csv(RAW, encoding='cp1252', nrows=0).columns]]),
    }
    with open(MARTS / "data_profile.json", "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    print(f"Wrote marts to {MARTS}")


if __name__ == "__main__":
    main()
