# Supply Chain Delivery Risk Prediction & Performance Analytics

## 1. Project Summary

**Project name:** Supply Chain Risk Intelligence

**Dataset:** DataCo Smart Supply Chain for Big Data Analysis

**Main objective:** Build an end-to-end data portfolio project that analyzes delivery performance, supply chain risk, profitability, and late delivery prediction using a ready-to-process public dataset.

This project is intentionally **not sentiment analysis** and **not scraping-based**. It uses an existing structured dataset and focuses on practical data work: cleaning, transformation, business KPI analysis, predictive modeling, and dashboard storytelling.

---

## 2. Business Problem

A supply chain company needs to reduce late deliveries, understand where operational risk comes from, and identify which markets, products, customers, and shipping modes affect profitability and customer experience.

The project answers these business questions:

1. Which shipments are most likely to be late?
2. Which shipping modes, regions, and markets create the highest delivery risk?
3. Which product categories and customer segments drive revenue and profit?
4. Are there high-revenue segments with weak margins or high delay risk?
5. Can we predict late delivery risk before the order is completed?
6. What business actions should be prioritized to improve service level and profitability?

---

## 3. Dataset Location

Raw files are stored locally in:

```text
D:\Project_Portofolio\supply-chain-risk-intelligence\data\raw\
```

Files:

```text
DataCoSupplyChainDataset.csv
DescriptionDataCoSupplyChain.csv
tokenized_access_logs.csv
```

Initial inspection of the main CSV:

- Rows: 180,519
- Columns: 53
- Main target column: `Late_delivery_risk`
- Primary delivery status column: `Delivery Status`

Initial target distribution:

- Late delivery risk = 1: 98,977
- Late delivery risk = 0: 81,542
- Late delivery rate: approximately 54.83%

---

## 4. Portfolio Positioning

This project should be framed as a **Data Analyst + Data Scientist + BI** project.

### Data Engineering

- Raw CSV ingestion
- Column standardization
- Data cleaning
- Date parsing
- PII removal / exclusion
- Feature engineering
- Dashboard-ready mart generation

### Data Analysis

- Delivery KPI analysis
- Shipping mode comparison
- Market and region performance
- Product category profitability
- Customer segment analysis
- Discount and margin analysis

### Data Science

- Late delivery classification
- Risk probability scoring
- Feature importance analysis
- Model evaluation
- Operational threshold discussion

### Business Intelligence

- Executive KPI dashboard
- Delivery risk dashboard
- Profitability dashboard
- Model insight page
- Recommendation page

---

## 5. Recommended Folder Structure

```text
supply-chain-risk-intelligence/
├── BLUEPRINT.md
├── README.md
├── data/
│   ├── raw/
│   │   ├── DataCoSupplyChainDataset.csv
│   │   ├── DescriptionDataCoSupplyChain.csv
│   │   └── tokenized_access_logs.csv
│   ├── processed/
│   │   └── orders_clean.csv
│   └── marts/
│       ├── delivery_kpis.csv
│       ├── profitability_kpis.csv
│       ├── region_shipping_kpis.csv
│       ├── category_performance.csv
│       └── model_scoring_sample.csv
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_eda_supply_chain.ipynb
│   └── 03_late_delivery_modeling.ipynb
├── scripts/
│   ├── prepare_data.py
│   ├── train_model.py
│   └── build_dashboard_data.py
├── sql/
│   ├── 01_clean_orders.sql
│   └── 02_business_kpi_marts.sql
├── dashboard/
│   ├── index.html
│   └── assets/
│       └── dashboard_data.json
└── docs/
    ├── data_dictionary.md
    ├── methodology.md
    └── limitations.md
```

---

## 6. Analysis Scope

### A. Delivery Performance

Core KPIs:

- Total orders
- Late delivery rate
- On-time delivery rate
- Average actual shipping days
- Average scheduled shipping days
- Average delay gap
- Late delivery count by shipping mode
- Late delivery count by market and region

Suggested charts:

- Delivery status distribution
- Late delivery rate by shipping mode
- Late delivery rate by market
- Late delivery rate by product category
- Monthly late delivery trend
- Top risky destination countries/cities

---

### B. Profitability Analytics

Core KPIs:

- Total sales
- Total profit
- Average profit per order
- Average profit margin
- Loss-making order count
- Loss-making order rate
- High-revenue low-margin segments

Suggested charts:

- Sales vs profit by market
- Profit by product category
- Profit margin by customer segment
- Discount impact on profit
- Top profitable products
- Worst loss-making categories

---

### C. Customer and Region Analytics

Core KPIs:

- Orders by customer segment
- Revenue by customer segment
- Late delivery rate by customer segment
- Market-level performance
- Country-level performance
- Product category demand by region

Suggested charts:

- Customer segment revenue share
- Customer segment delay risk
- Market performance ranking
- Region/category matrix
- Order volume by country

---

### D. Predictive Modeling

Target column:

```text
Late_delivery_risk
```

Target meaning:

- `1`: order has late delivery risk
- `0`: order does not have late delivery risk

Recommended models:

1. Logistic Regression as interpretable baseline
2. Random Forest as stronger benchmark
3. XGBoost or LightGBM only if dependencies are stable

Model evaluation metrics:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion matrix

Business metric priority:

- Prioritize **recall** for the late-delivery class.
- Reason: in supply chain operations, missing a risky shipment is usually worse than over-flagging a safe shipment.

Model output:

```text
delivery_risk_probability
risk_level = Low / Medium / High
```

Example risk level logic:

```text
Low: probability < 0.40
Medium: 0.40 <= probability < 0.70
High: probability >= 0.70
```

---

## 7. Feature Engineering Plan

Potential features:

### Date Features

- Order year
- Order month
- Order quarter
- Order day of week
- Shipping year/month if available

### Shipping Features

- Actual shipping days
- Scheduled shipping days
- Shipping gap = actual days - scheduled days
- Shipping mode

Important modeling warning:

If `Days for shipping (real)` directly determines `Late_delivery_risk`, it may cause target leakage. Build two model versions:

1. **Diagnostic model:** includes actual shipping days to explain historical delay patterns.
2. **Operational prediction model:** excludes post-shipment fields that would not be known at order time.

### Financial Features

- Sales per customer
- Benefit per order
- Order item total
- Order item discount
- Order item discount rate
- Profit margin proxy

### Product Features

- Category name
- Department name
- Product price
- Product category

### Customer and Geography Features

- Customer segment
- Market
- Order region
- Order country
- Customer country

---

## 8. Dashboard Blueprint

### Tab 1 — Executive Overview

Purpose: recruiter/interviewer can understand the project in 30 seconds.

Components:

- Total orders
- Total sales
- Total profit
- Late delivery rate
- Average shipping delay
- Key insight cards
- Top 3 operational risks
- Top 3 business recommendations

---

### Tab 2 — Delivery Risk

Purpose: show operational performance and delivery bottlenecks.

Components:

- Delivery status distribution
- Late delivery rate by shipping mode
- Late delivery rate by market
- Late delivery trend over time
- Top risky regions/countries
- Risk matrix: shipping mode x market

---

### Tab 3 — Profitability

Purpose: connect operations to business impact.

Components:

- Sales by category
- Profit by category
- Profit margin by market
- Loss-making order analysis
- Discount vs profit relationship
- High revenue / low margin segments

---

### Tab 4 — Customer and Region

Purpose: identify where service and business value differ.

Components:

- Revenue by customer segment
- Late delivery rate by customer segment
- Market performance table
- Country performance ranking
- Customer segment profitability

---

### Tab 5 — Model Insights

Purpose: prove data science competency.

Components:

- Model performance cards
- Confusion matrix
- ROC-AUC value
- Precision / recall / F1 comparison
- Feature importance
- Risk score distribution
- Example high-risk orders

---

### Tab 6 — Recommendations

Purpose: show business thinking, not just charts.

Recommended insight structure:

1. **Shipping Mode Optimization**
   - Identify shipping modes with high delay rate.
   - Recommend SLA review or routing adjustment.

2. **Market Intervention Priority**
   - Identify markets with high volume and high delay risk.
   - Prioritize operational improvement where impact is largest.

3. **Profitability Protection**
   - Identify categories or regions with low margin and high delay.
   - Recommend discount control or fulfillment cost review.

4. **Risk-Based Operations**
   - Use the late delivery risk model to flag orders before fulfillment.
   - High-risk orders can receive earlier monitoring or shipping upgrade.

---

## 9. Script Execution Plan

### Step 1 — Prepare clean dataset

```bash
python scripts/prepare_data.py
```

Expected outputs:

```text
data/processed/orders_clean.csv
data/marts/delivery_kpis.csv
data/marts/profitability_kpis.csv
data/marts/region_shipping_kpis.csv
data/marts/category_performance.csv
```

### Step 2 — Train baseline model

```bash
python scripts/train_model.py
```

Expected outputs:

```text
data/marts/model_metrics.json
data/marts/feature_importance.csv
data/marts/model_scoring_sample.csv
```

### Step 3 — Build dashboard data

```bash
python scripts/build_dashboard_data.py
```

Expected output:

```text
dashboard/assets/dashboard_data.json
```

### Step 4 — Run dashboard locally

```bash
python -m http.server 8000 -d dashboard
```

Open:

```text
http://localhost:8000
```

---

## 10. README Angle

Opening paragraph should be concrete, not generic.

Suggested draft:

> This project analyzes 180,519 supply chain orders from the DataCo Smart Supply Chain dataset to identify late delivery risk, profitability gaps, and operational bottlenecks. The analysis combines KPI marts, delivery performance analytics, and a late-delivery classification model to support risk-based fulfillment decisions.

Avoid generic wording like:

- “In today’s data-driven world”
- “Leveraging cutting-edge technology”
- “Unlocking insights”
- “Seamless dashboard experience”

---

## 11. Limitations to Document

This section should exist in the final README and docs.

Key limitations:

1. The dataset is public and historical, not connected to a live supply chain system.
2. Some columns may create target leakage for prediction if they are only known after shipment.
3. The model should be interpreted as a portfolio-grade decision support prototype, not a production SLA engine.
4. No real-time routing, carrier capacity, warehouse capacity, or weather data is included.
5. Financial fields are analyzed as provided by the dataset and may not represent audited company-level financials.

---

## 12. Final Deliverables

Minimum viable portfolio deliverables:

- Cleaned dataset
- KPI marts
- EDA notebook
- Late delivery model
- Static dashboard
- README
- Methodology documentation
- Limitations documentation

Best version deliverables:

- Deployed dashboard on Vercel
- GitHub repository with reproducible scripts
- Model metrics and feature importance
- Business recommendation page
- Short project write-up for LinkedIn/CV

---

## 13. Suggested CV Bullet

> Built an end-to-end supply chain analytics project using 180K+ order records, combining delivery KPI analysis, profitability segmentation, and late-delivery risk prediction to support operational decision-making through an interactive dashboard.

---

## 14. Next Implementation Step

Start with:

```text
scripts/prepare_data.py
```

The script should produce the first clean dataset and KPI marts before any dashboard work begins.
