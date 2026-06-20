# Week 1 and Week 2 Completion Report

## Source data quality

- Raw dataset: 541,909 rows and 8 columns.
- Cleaned Week 1 transaction dataset: 392,692 rows after removing duplicate rows, missing customer IDs/descriptions, cancelled invoices, negative quantities, and non-positive prices.
- Date range: 2010-12-01 to 2011-12-09.
- Countries represented after cleaning: 37.

## Week 1 completed

- Dataset selected: UCI Online Retail transaction data.
- EDA completed for distributions, missing values, duplicate records, country mix, invoice dates, quantity, unit price, and sales value.
- Missing values handled:
  - `CustomerID` rows are removed for customer-level RFM, churn, and segmentation because they cannot be linked to a customer.
  - Missing `Description` rows are removed from item-level modeling.
  - Invalid transactions with `Quantity <= 0` or `UnitPrice <= 0` are excluded from demand and revenue modeling.
- Feature engineering completed: `TotalPrice`, daily sales series, RFM customer metrics, and segmentation-ready customer table.
- Customer segmentation assets are available in `data/cleaned/rfm_customers.csv`.
- Baseline demand forecast output is available in `exports/forecast_results.csv`.

## Week 2 completed

- Hybrid demand forecast created in `exports/week2_hybrid_forecast.csv`.
- Churn-risk model created using customer RFM and behavioral features.
- Inventory reorder recommendations created in `exports/week2_inventory_recommendations.csv`.
- Feature importance exported to `exports/week2_feature_importance.csv`.
- Drift checks exported to `exports/week2_drift_checks.csv`.
- Automated retraining trigger logic documented below.

## Week 2 metrics

| Metric | Value |
|---|---:|
| Churn model AUC-ROC | 0.717 |
| Churn model F1 | 0.640 |
| Churn model accuracy | 0.647 |
| Test customers | 843 |
| High-risk customers | 1,072 |
| Recent hybrid forecast MAPE | 0.314 |
| Inventory SKUs scored | 2,953 |
| Drift flags raised | 0 |

## Feature importance

| feature               |   importance_mean |   importance_std |
|:----------------------|------------------:|-----------------:|
| recency               |        0.00403321 |       0.0082048  |
| orders_per_active_day |       -0.00189798 |       0.00120973 |
| avg_order_value       |       -0.00260973 |       0.00812899 |
| tenure_days           |       -0.00260973 |       0.00264188 |
| frequency             |       -0.00403321 |       0.00206828 |
| unique_products       |       -0.00474496 |       0.00424402 |
| active_days           |       -0.00474496 |       0.00561431 |
| monetary              |       -0.0059312  |       0.00671038 |

## Retraining policy

- Rebuild features daily after new transaction ingestion.
- Retrain churn and forecasting models weekly, or immediately if a drift check changes by more than 20%.
- Log model metrics, input data dates, and exported prediction files with MLflow.
- Promote a model only when validation metrics improve or business rules require a refresh.
