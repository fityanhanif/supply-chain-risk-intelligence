# CV and Portfolio Summary

## One-line project description

Built an end-to-end supply chain risk intelligence dashboard using 180K+ order records, Python KPI marts, and a leakage-aware late-delivery prediction model deployed as a static Vercel dashboard.

## CV bullet options

- Built a Python data pipeline for 180,519 supply chain orders, transforming raw CSV data into cleaned KPI marts, model outputs, and dashboard-ready JSON assets.
- Developed a leakage-aware late-delivery risk model, excluding post-shipment fields and prioritizing late-class recall for realistic pre-fulfillment risk scoring.
- Designed an interactive Chart.js dashboard on Vercel to monitor delivery risk, profitability, customer-region performance, feature importance, and operational recommendations.
- Analyzed delivery and profitability patterns across shipping modes, markets, regions, product categories, and customer segments to identify high-risk and low-margin segments.

## Recruiter-friendly project positioning

This project shows the full workflow expected from a data analyst or junior data scientist: data cleaning, KPI design, exploratory analysis, machine learning, model interpretation, dashboard storytelling, and deployment. The main strength is not only the model score, but also the business framing around delivery risk, profit quality, target leakage prevention, and operational action.

## Interview talking points

1. **Business problem:** reduce late deliveries and identify risky fulfillment segments before they become customer-facing service problems.
2. **Data work:** cleaned raw DataCo order data, standardized columns, engineered dates, removed PII-like fields, and generated reusable marts.
3. **Modeling decision:** excluded leakage fields such as final delivery status and actual shipping days to keep the model realistic for pre-fulfillment scoring.
4. **Model selection:** selected Random Forest using a business-weighted composite score focused on late-class recall, F1, and ROC-AUC.
5. **Dashboard value:** connected delivery risk, profitability, customer segments, model insights, and recommendations in one static dashboard.
6. **Next iteration:** threshold tuning, PR-AUC, calibration, cost-sensitive evaluation, and additional live operational features such as warehouse backlog, carrier capacity, route distance, weather, and inventory.

## Links

- GitHub repository: https://github.com/fityanhanif/supply-chain-risk-intelligence
- Live dashboard: https://supply-chain-risk-intelligence-two.vercel.app
