# Release Notes

## Supply Chain Risk Intelligence MVP

Local project path:

`D:\Project_Portofolio\supply-chain-risk-intelligence`

## Included deliverables

- Reproducible Python data pipeline
- Cleaned dataset and KPI marts
- Leakage-aware late delivery risk model
- Model metrics and feature importance
- Static dashboard with Chart.js
- Dashboard JSON generated from marts
- EDA notebook
- README and documentation
- Static deployment config for Vercel

## Verified commands

```bash
python scripts/prepare_data.py
python scripts/train_model.py
python scripts/build_dashboard_data.py
python -m http.server 8000 -d dashboard
```

## Main model result

Best model: Random Forest

- Accuracy: 69.57%
- Precision late class: 81.35%
- Recall late class: 57.73%
- F1 late class: 67.54%
- ROC-AUC: 75.63%

## Dashboard entrypoint

Local:

```text
http://localhost:8000
```

Static files:

- `dashboard/index.html`
- `dashboard/assets/dashboard_data.json`

## Deployment note

This repo is ready for GitHub and Vercel, but it has not been pushed or deployed yet. Push/deploy should be done only when explicitly requested.
