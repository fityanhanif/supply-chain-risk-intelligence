# Limitations

## Dataset scope

The dataset is public and historical. It is not connected to a live supply chain system, carrier API, warehouse management system, or real-time order stream.

## Target leakage risk

Some columns directly describe delivery outcomes. Using them in a predictive model would inflate model performance and make the model unrealistic for pre-fulfillment decisions.

The operational model excludes post-shipment leakage fields such as:

- `delivery_status`
- `days_for_shipping_real`
- `shipping_gap`
- `shipping_date_dateorders`
- `order_status`

These fields can still be used for historical diagnostic analysis, but not for a realistic pre-shipment prediction model.

## Model maturity

The model is a portfolio-grade decision-support prototype. It is not a production SLA engine.

Before production use, the model would need:

- threshold tuning with business cost assumptions
- monitoring of false positives and false negatives
- drift monitoring by market, region, product category, and shipping mode
- retraining schedule
- operational feedback loop from fulfillment teams

## Missing operational context

The dataset does not include several variables that would matter in real logistics:

- carrier capacity
- warehouse capacity
- live inventory constraints
- route distance
- weather
- holidays
- customs delays
- traffic conditions
- service-level agreements by carrier

## Financial interpretation

Financial fields are analyzed as provided by the dataset. They should be interpreted as dataset-level sales and benefit proxies, not audited company-level financial statements.

## Access logs

`tokenized_access_logs.csv` is available in the raw data folder, but the current MVP focuses on order-level supply chain risk. Access logs can be added later for product traffic or demand signal analysis.
