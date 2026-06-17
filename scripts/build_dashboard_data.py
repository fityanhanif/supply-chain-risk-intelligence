"""Build dashboard/assets/dashboard_data.json from KPI marts."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MARTS = ROOT / "data" / "marts"
DASH_ASSETS = ROOT / "dashboard" / "assets"


def read_csv(name: str) -> pd.DataFrame:
    path = MARTS / name
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def clean_value(v):
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        if np.isnan(v) or np.isinf(v):
            return None
        return float(v)
    if pd.isna(v):
        return None
    return v


def records(df: pd.DataFrame, limit: int | None = None) -> list[dict]:
    if limit is not None:
        df = df.head(limit)
    return [{k: clean_value(v) for k, v in row.items()} for row in df.to_dict(orient="records")]


def pct(x: float) -> float:
    return round(float(x) * 100, 2)


def main() -> None:
    DASH_ASSETS.mkdir(parents=True, exist_ok=True)

    with open(MARTS / "data_profile.json", "r", encoding="utf-8") as f:
        profile = json.load(f)

    delivery = read_csv("delivery_kpis.csv")
    region_shipping = read_csv("region_shipping_kpis.csv")
    category = read_csv("category_performance.csv")
    profitability = read_csv("profitability_kpis.csv")
    customer_market = read_csv("customer_market_kpis.csv")
    monthly = read_csv("monthly_delivery_trend.csv")
    feature_importance = read_csv("feature_importance.csv")
    scoring = read_csv("model_scoring_sample.csv")
    with open(MARTS / "model_metrics.json", "r", encoding="utf-8") as f:
        model_metrics = json.load(f)

    total_orders = profile["clean_rows"]
    total_sales = profile["total_sales"]
    total_profit = profile["total_profit"]
    late_rate = profile["late_delivery_rate"]
    avg_margin = profile["avg_profit_margin"]

    risky_regions = (
        region_shipping[region_shipping["orders"] >= 500]
        .sort_values(["late_rate", "orders"], ascending=[False, False])
        .head(10)
    )
    high_revenue_low_margin = (
        profitability[profitability["orders"] >= 100]
        .sort_values(["sales", "profit_margin"], ascending=[False, True])
        .head(10)
    )
    top_categories = category.sort_values("sales", ascending=False).head(10)
    loss_categories = category[category["profit"] < 0].sort_values("profit", ascending=True).head(10)

    best_name = model_metrics["best_model"]
    best_metrics = model_metrics["metrics"][best_name]

    insights = [
        {
            "title": "Late delivery is the main operational risk",
            "metric": f"{pct(late_rate)}% late-risk rate",
            "detail": "More than half of historical orders are flagged as late delivery risk, so service-level control should be treated as a core operating KPI.",
            "priority": "Critical",
        },
        {
            "title": "Standard Class dominates shipment volume",
            "metric": f"{int(delivery.sort_values('orders', ascending=False).iloc[0]['orders']):,} orders",
            "detail": "The highest-volume shipping mode has the largest operational leverage. Improvements here move the portfolio-level KPI fastest.",
            "priority": "High Impact",
        },
        {
            "title": "Profit and delivery risk must be viewed together",
            "metric": f"${total_profit:,.0f} total benefit",
            "detail": "Some segments generate revenue but carry margin pressure and delay risk. The dashboard separates revenue growth from profit quality.",
            "priority": "Strategic",
        },
        {
            "title": "Operational prediction should avoid leakage",
            "metric": f"{pct(best_metrics['recall_late'])}% recall",
            "detail": "The selected model excludes post-shipment fields such as actual shipping days and delivery status, making the score closer to a real pre-fulfillment use case.",
            "priority": "Model Governance",
        },
    ]

    recommendations = [
        {
            "title": "Review SLA and routing for high-volume risky shipping modes",
            "priority": "Critical",
            "current_metric": f"{pct(late_rate)}% late-risk baseline",
            "target": "Reduce late-risk rate by 5-8 percentage points in the first pilot lanes.",
            "actions": [
                "Start with mode x market combinations with high order count and high late rate.",
                "Compare scheduled days against actual shipping gaps to identify unrealistic SLA promises.",
                "Escalate high-risk orders before fulfillment using the model score.",
            ],
        },
        {
            "title": "Protect margin in high-revenue low-margin segments",
            "priority": "High Impact",
            "current_metric": f"{pct(avg_margin)}% average profit margin proxy",
            "target": "Reduce avoidable loss-making orders and discount leakage.",
            "actions": [
                "Audit categories where discounts are high but profit margin is weak.",
                "Separate growth segments from segments that only look good by sales volume.",
                "Tie discount policy to fulfillment cost and delay risk.",
            ],
        },
        {
            "title": "Deploy a risk queue for operations teams",
            "priority": "Strategic",
            "current_metric": f"{pct(best_metrics['recall_late'])}% late-class recall on test data",
            "target": "Flag high-risk orders early enough for manual monitoring or shipping upgrade.",
            "actions": [
                "Use Low / Medium / High risk buckets instead of raw probability only.",
                "Monitor precision and false positives so the team does not get alert fatigue.",
                "Retrain periodically when lanes, carriers, and customer mix change.",
            ],
        },
    ]

    data = {
        "meta": {
            "project": "Supply Chain Risk Intelligence",
            "source": "DataCo Smart Supply Chain dataset",
            "generated_from": "scripts/build_dashboard_data.py",
        },
        "kpis": {
            "total_orders": total_orders,
            "total_sales": total_sales,
            "total_profit": total_profit,
            "late_delivery_rate": late_rate,
            "on_time_rate": 1 - late_rate,
            "avg_profit_margin": avg_margin,
            "best_model": best_name,
            "model_recall_late": best_metrics["recall_late"],
            "model_f1_late": best_metrics["f1_late"],
            "model_roc_auc": best_metrics["roc_auc"],
        },
        "delivery_status": profile["delivery_status"],
        "shipping_mode": records(delivery.sort_values("orders", ascending=False)),
        "markets": profile["market"],
        "monthly_trend": records(monthly),
        "risky_regions": records(risky_regions),
        "top_categories": records(top_categories),
        "loss_categories": records(loss_categories),
        "profitability": records(profitability.head(30)),
        "high_revenue_low_margin": records(high_revenue_low_margin),
        "customer_market": records(customer_market.sort_values("sales", ascending=False).head(30)),
        "feature_importance": records(feature_importance, 25),
        "model_metrics": model_metrics,
        "scoring_sample": records(scoring.head(50)),
        "insights": insights,
        "recommendations": recommendations,
    }

    out = DASH_ASSETS / "dashboard_data.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, allow_nan=False)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
