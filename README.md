# RetailPulse AI - Customer Analytics and Demand Forecasting

RetailPulse AI is an end-to-end data science project for retail demand planning, customer segmentation, churn-risk detection, and inventory optimization. The project follows the Zidio Data Science and Analytics brief for the first two weeks of work and uses the provided Online Retail dataset.

## Project Objective

Retail businesses lose revenue when demand is poorly forecasted, customers at risk are missed, and stock decisions are made without data. This project turns transaction data into practical analytics outputs:

- Cleaned retail sales data ready for modeling
- RFM-based customer segmentation
- Daily demand forecasting outputs
- Churn-risk scores for customers
- Inventory reorder recommendations
- Drift checks and retraining policy

## Dataset Used

The project uses the provided `online_retail.csv` and `OnlineRetail.xlsx` files.

| Item | Value |
|---|---:|
| Raw rows | 541,909 |
| Raw columns | 8 |
| Cleaned transaction rows | 392,692 |
| Date range | 2010-12-01 to 2011-12-09 |
| Countries | 38 |
| Duplicate rows found | 5,268 |
| Missing descriptions | 1,454 |
| Missing customer IDs | 135,080 |
| Cancelled invoices | 9,288 |
| Negative quantity rows | 10,624 |
| Non-positive unit price rows | 2,517 |

## Missing Value and Cleaning Strategy

The project intentionally keeps the data-quality issues visible in the documentation and handles them before modeling:

- Rows with missing `CustomerID` are removed from RFM, segmentation, and churn modeling because they cannot be assigned to a known customer.
- Rows with missing `Description` are removed from product and inventory analysis.
- Duplicate rows are removed during cleaning.
- Cancelled invoices and rows with `Quantity <= 0` are excluded from demand forecasting and inventory recommendations.
- Rows with `UnitPrice <= 0` are excluded because they do not represent valid revenue transactions.
- `InvoiceDate` is parsed as a datetime field.
- `TotalPrice = Quantity * UnitPrice` is created for revenue analysis.

## Repository Structure

```text
RetailPulse-AI/
|-- data/
|   |-- raw/
|   |-- cleaned/
|-- exports/
|-- models/
|-- notebooks/
|-- reports/
|-- scripts/
|-- mlflow.db
|-- requirements.txt
|-- README.md
```

## Week 1 Status - Completed

Week 1 focused on data exploration and preparation.

| Day | Task from brief | Status | Output |
|---:|---|---|---|
| 1 | Dataset selection and initial EDA | Completed | `notebooks/01_eda.ipynb` |
| 2 | Data cleaning and feature engineering | Completed | `data/cleaned/cleaned_retail.csv` |
| 2 | Data validation checks | Completed | Cleaning rules documented in this README |
| 3 | Customer segmentation with K-Means and DBSCAN | Completed | `notebooks/02_customer_segmentation.ipynb`, `data/cleaned/rfm_customers.csv` |
| 4 | Time-series preparation | Completed | `notebooks/03_time_series_preparation.ipynb` |
| 5 | Baseline forecasting | Completed | `notebooks/04_demand_forecasting.ipynb`, `exports/forecast_results.csv` |
| 6 | LSTM implementation | Completed | `notebooks/05_lstm_model_implementation.ipynb`, `models/lstm_model.pth` |
| 7 | Week 1 checkpoint | Completed | `reports/week1_week2_completion_report.md` |

## Week 2 Status - Completed

Week 2 focused on advanced modeling, churn prediction, inventory logic, drift checks, and retraining planning.

| Day | Task from brief | Status | Output |
|---:|---|---|---|
| 8 | Hybrid forecasting model | Completed | `notebooks/06_hybrid_forecasting_inventory.ipynb` |
| 9 | Churn prediction model | Completed | `notebooks/07_churn_xgboost_optuna.ipynb` |
| 10 | Inventory optimization logic | Completed | `notebooks/06_hybrid_forecasting_inventory.ipynb` |
| 11 | Feature importance analysis | Completed | `notebooks/07_churn_xgboost_optuna.ipynb` |
| 12 | Drift detection setup | Completed | `notebooks/08_drift_evidently.ipynb`, `reports/week2_evidently_drift_report.html` |
| 13 | Automated retraining pipeline plan | Completed | `dags/retraining_pipeline.py` |
| 14 | Week 2 checkpoint | Completed | Notebooks 06-08 & DAG |

## Week 3 Status - Completed

Week 3 focuses on building the interactive Streamlit dashboard.

| Day | Task from brief | Status | Output |
|---:|---|---|---|
| 15 | Streamlit dashboard skeleton | Completed | `app/main.py` |
| 16 | Demand forecasting visualizations | Completed | `app/pages/01_demand_forecasting.py` |
| 17 | Customer segmentation dashboard | Completed | `app/pages/02_customer_segmentation.py` |
| 18 | Inventory optimization UI | Completed | `app/pages/03_inventory_optimization.py` |
| 19 | Real-time metrics and alerts | Completed | `app/pages/04_alerts_and_exports.py` |
| 20 | Export functionality | Completed | `app/pages/04_alerts_and_exports.py` |
| 21 | Week 3 checkpoint | Completed | Full Dashboard |

## Week 2 Model Summary

The Week 2 pipeline is reproducible from:

```bash
python scripts/week2_pipeline.py
```

Generated outputs:

- `exports/week2_hybrid_forecast.csv`
- `exports/week2_customer_features.csv`
- `exports/week2_churn_predictions.csv`
- `exports/week2_inventory_recommendations.csv`
- `exports/week2_feature_importance.csv`
- `exports/week2_drift_checks.csv`
- `reports/week1_week2_completion_report.md`

Current Week 2 checkpoint metrics:

| Metric | Value |
|---|---:|
| Customers scored for churn | 3,370 |
| Churn model AUC-ROC | 0.715 |
| Churn model F1 | 0.644 |
| High-risk customers identified | 1,039 |
| Inventory SKUs scored | 2,953 |
| Recent hybrid forecast MAPE | 0.314 |
| Drift flags raised | 0 |

## Technology Stack

| Layer | Tools |
|---|---|
| Language | Python |
| Data processing | Pandas, NumPy |
| Machine learning | Scikit-learn, PyTorch, Prophet-ready outputs |
| Segmentation | K-Means, DBSCAN |
| Experiment tracking | MLflow |
| Dashboard roadmap | Streamlit |
| Monitoring roadmap | Evidently AI-style drift checks |

## How to Run Step-by-Step

This project is built and optimized for Windows. Follow these exact steps in your terminal to reproduce the entire 3-week pipeline.

### Step 1: Environment Setup
First, navigate to the project directory, create a virtual environment, activate it, and install all required libraries.
```powershell
# 1. Open PowerShell and navigate to the folder
cd "d:\college 3rd year\zidio\RetailPulseAI-Zidio"

# 2. Create the virtual environment
python -m venv .venv

# 3. Activate the virtual environment
.venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt
```

### Step 2: Week 1 - Data Prep & Baseline Models
Week 1 is entirely notebook-based. You must run these notebooks in order to generate the cleaned datasets and the baseline Prophet/LSTM models.
1. Open VS Code.
2. Ensure your Jupyter Kernel is set to `.venv`.
3. Open and click **"Run All"** on the following notebooks in order:
   - `notebooks/01_eda.ipynb`
   - `notebooks/02_customer_segmentation.ipynb`
   - `notebooks/03_time_series_preparation.ipynb`
   - `notebooks/04_demand_forecasting.ipynb`
   - `notebooks/05_lstm_model_implementation.ipynb`

To view the Week 1 MLflow logging and Prophet models, open a terminal and run:
```powershell
.venv\Scripts\python.exe -m mlflow ui --backend-store-uri sqlite:///mlflow.db
```
*Then open `http://127.0.0.1:5000` in your browser. Press `Ctrl+C` in the terminal to stop the server when done.*

### Step 3: Week 2 - Advanced Pipeline & Models
Run the core feature engineering pipeline script, which generates customer behavior features and historic hybrid forecasts.
```powershell
# Run the core Week 2 pipeline
.venv\Scripts\python.exe scripts/week2_pipeline.py
```

Next, open and **"Run All"** on the advanced Week 2 notebooks to train XGBoost, run Optuna, and generate Evidently AI drift reports:
- `notebooks/06_hybrid_forecasting_inventory.ipynb`
- `notebooks/07_churn_xgboost_optuna.ipynb`
- `notebooks/08_drift_evidently.ipynb`

*Note: You can view the generated drift HTML report by double-clicking `reports/week2_evidently_drift_report.html` in your file explorer.*

If you need to verify the Automated Retraining DAG (Day 13 Checkpoint), you can validate the Airflow code using:
```powershell
.venv\Scripts\python.exe dags/retraining_pipeline.py
```

### Step 4: Week 3 - Interactive Dashboards
To launch the final Streamlit Executive Dashboard (Days 15-17) with the Demand Forecasting and Churn Risk visualizations, run:
```powershell
.venv\Scripts\python.exe -m streamlit run app/main.py
```
*The dashboard will automatically open in your default web browser at `http://localhost:8501`. Use the sidebar to navigate between pages.*

## Current Project Milestone

- Week 1: Completed
- Week 2: Completed (Refactored to XGBoost, Optuna, Evidently, Airflow)
- Week 3: Completed (Streamlit UI with Exports and Alerts)
- Week 4: Deployment and production polish pending

## Submission Notes

This README now reflects the Zidio brief requirements for Week 1 and Week 2, including missing-value handling, cleaned data preparation, modeling outputs, and documented next steps.
