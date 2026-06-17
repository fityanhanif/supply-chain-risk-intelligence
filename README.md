# Supply Chain Risk Intelligence

This project analyzes **180,519 supply chain orders** from the DataCo Smart Supply Chain dataset to identify delivery risk, profitability gaps, and operational bottlenecks. The current pipeline cleans raw order data, builds KPI marts, trains a late-delivery risk model, and exports dashboard-ready JSON.

## What this project answers

1. Which shipments are most likely to be late?
2. Which shipping modes, markets, and regions create the highest delivery risk?
3. Which product categories and customer segments drive sales and profit?
4. Are there high-revenue segments with weak margins or high delay risk?
5. Can late delivery risk be scored before fulfillment?
6. What operational actions should be prioritized?

## Key numbers from the dataset

- Orders analyzed: **180,519**
- Columns in raw order dataset: **53**
- Late delivery risk orders: **98,977**
- Late delivery risk rate: **54.83%**
- Total sales: **$36.78M**
- Total benefit/profit proxy: **$3.97M**
- Largest shipping mode by raw order records: **Standard Class** with 107,752 records
- Largest market by raw order records: **LATAM** with 51,594 records

## Project structure

```text
supply-chain-risk-intelligence/
├── BLUEPRINT.md
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                  # original CSV files
│   ├── processed/            # cleaned anonymized order data
│   └── marts/                # KPI tables and model outputs
├── dashboard/
│   ├── index.html
│   └── assets/dashboard_data.json
├── docs/
│   ├── data_dictionary.md
│   ├── methodology.md
│   └── limitations.md
├── models/
│   └── late_delivery_risk_model.joblib
├── notebooks/
│   └── 01_eda_supply_chain.ipynb
└── scripts/
    ├── prepare_data.py
    ├── train_model.py
    └── build_dashboard_data.py
```

## Pipeline

### 1. Prepare data and KPI marts

```bash
python scripts/prepare_data.py
```

Outputs:

- `data/processed/orders_clean.csv`
- `data/marts/delivery_kpis.csv`
- `data/marts/profitability_kpis.csv`
- `data/marts/region_shipping_kpis.csv`
- `data/marts/category_performance.csv`
- `data/marts/customer_market_kpis.csv`
- `data/marts/monthly_delivery_trend.csv`
- `data/marts/data_profile.json`

### 2. Train late-delivery model

```bash
python scripts/train_model.py
```

Outputs:

- `models/late_delivery_risk_model.joblib`
- `data/marts/model_metrics.json`
- `data/marts/feature_importance.csv`
- `data/marts/model_scoring_sample.csv`

The model is built as an **operational prediction model**, so post-shipment leakage fields are excluded:

- `Delivery Status`
- `Days for shipping (real)`
- `shipping_gap`
- `shipping date (DateOrders)`
- `Order Status`

### 3. Build dashboard JSON

```bash
python scripts/build_dashboard_data.py
```

Output:

- `dashboard/assets/dashboard_data.json`

### 4. Run dashboard locally

```bash
python -m http.server 8000 -d dashboard
```

Open:

```text
http://localhost:8000
```

## Model result

Two baseline models are trained and compared with business priority on late-class recall.

Best model selected: **Random Forest**

- Accuracy: **69.57%**
- Precision for late-risk class: **81.35%**
- Recall for late-risk class: **57.73%**
- F1 for late-risk class: **67.54%**
- ROC-AUC: **75.63%**

Business interpretation: the baseline model is useful for a portfolio-grade risk scoring prototype, but recall still needs improvement before production use. In supply chain operations, missed risky shipments are costly, so recall should be tuned further with thresholds, class weights, and operational feedback.

## Skills demonstrated

### Data Engineering

Built a reproducible Python pipeline that transforms raw CSV data into cleaned datasets, KPI marts, and dashboard-ready JSON. PII-like customer fields are removed from the processed dataset.

### Data Analysis

Analyzed delivery performance, shipping modes, markets, regions, categories, customer segments, profit, margin, and loss-making orders.

### Data Science

Trained baseline late-delivery classification models with leakage-aware feature selection, model evaluation, feature importance, and risk-level scoring.

### Business Intelligence

Designed the project around executive KPIs, delivery risk monitoring, profitability segmentation, model insights, and action-oriented recommendations.

## Data source

Dataset: **DataCo Smart Supply Chain for Big Data Analysis**

Local raw files:

- `data/raw/DataCoSupplyChainDataset.csv`
- `data/raw/DescriptionDataCoSupplyChain.csv`
- `data/raw/tokenized_access_logs.csv`

## Limitations

- The dataset is public and historical, not connected to a live supply chain system.
- Some fields can create target leakage if used incorrectly. The operational model excludes post-shipment fields, but historical diagnostic analysis can still use them.
- The model is a portfolio-grade decision-support prototype, not a production SLA engine.
- No real carrier capacity, warehouse capacity, weather, route distance, or live inventory data is included.
- Financial fields are analyzed as provided by the dataset and may not represent audited company-level financials.

## Author

Fityan Hanif — Data Analyst / Data Scientist portfolio project.
