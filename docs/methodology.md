# Methodology

## Objective

The project turns the DataCo supply chain dataset into an end-to-end portfolio artifact: clean data, KPI marts, a late-delivery prediction model, dashboard data, and business recommendations.

## Data preparation

Raw order data is loaded from `data/raw/DataCoSupplyChainDataset.csv` with `cp1252` encoding. Column names are standardized to snake_case, date columns are parsed, and direct PII-like fields are removed from the processed dataset.

Removed fields include customer email, first name, last name, password, street, ZIP code, latitude, longitude, product image, and product description.

## Feature engineering

Key derived fields:

- `shipping_gap`: actual shipping days minus scheduled shipping days
- `is_late`: integer copy of the late-delivery target for easier analysis
- `is_loss_making`: order-level flag where benefit per order is below zero
- `profit_margin`: benefit per order divided by sales, clipped to avoid extreme display outliers
- `order_year`, `order_month`, `order_quarter`, `order_dayofweek`: date features from order date

## KPI marts

The project generates several marts:

- `delivery_kpis.csv`: delivery risk by shipping mode
- `region_shipping_kpis.csv`: delivery risk by market, region, and shipping mode
- `category_performance.csv`: sales, profit, and delay risk by product category
- `customer_market_kpis.csv`: customer segment performance by market
- `profitability_kpis.csv`: market, region, and category profitability
- `monthly_delivery_trend.csv`: monthly orders, late rate, sales, profit, and shipping gap

## Modeling approach

The target variable is `late_delivery_risk`.

Two baseline models are trained:

1. Logistic Regression
2. Random Forest

The selected model is based on a composite score that prioritizes recall for the late-delivery class, then F1 and ROC-AUC.

## Leakage control

For operational prediction, fields only known after shipment are excluded:

- `delivery_status`
- `days_for_shipping_real`
- `shipping_gap`
- `shipping_date_dateorders`
- `order_status`
- target and target duplicates

This makes the model less inflated but more realistic for pre-fulfillment risk scoring.

## Evaluation metrics

Metrics reported:

- Accuracy
- Precision for late-risk class
- Recall for late-risk class
- F1 for late-risk class
- ROC-AUC
- Confusion matrix

## Dashboard data

`scripts/build_dashboard_data.py` combines the KPI marts and model outputs into `dashboard/assets/dashboard_data.json`. The JSON is strict browser-safe JSON with NaN and infinity values converted to null.

## Business recommendation logic

Recommendations are based on three cross-cutting dimensions:

1. Delivery risk: where late delivery rate and order volume are both high.
2. Profitability: where high revenue does not translate into strong margin.
3. Model actionability: where risk scores can trigger early operational monitoring.
