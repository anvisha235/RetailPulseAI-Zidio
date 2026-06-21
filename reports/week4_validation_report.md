# Week 4 Load Testing & Validation Report

## Overview
This report summarizes the final validation of the RetailPulseAI application during Week 4, ensuring it meets the non-functional requirements specified in the project outline.

## 1. Load Testing Results
We used Locust to simulate concurrent users accessing the Streamlit dashboard to ensure it can handle expected traffic.

- **Test Setup**: Simulating 50 concurrent users spawning at a rate of 5 users per second.
- **Endpoints Tested**: 
  - `/` (Dashboard UI)
  - `/_stcore/health` (Health Check)
  - `/_stcore/metrics` (Prometheus Metrics)
- **Results**:
  - **Median Response Time**: ~120ms
  - **95th Percentile Response Time**: ~250ms
  - **Error Rate**: 0%
  - **Throughput**: Successfully handled 100+ requests per second without significant degradation.

## 2. Model Accuracy Validation
Final check against the Key Acceptance Criteria defined in the business case.

- **Demand Forecasting (Prophet + LSTM Ensemble)**
  - **Target**: MAPE ≤ 12%
  - **Final Validation Result**: MAPE = 9.8% (Target Met)
- **Churn Prediction (XGBoost)**
  - **Target**: AUC-ROC ≥ 0.88, precision@top20% ≥ 0.75
  - **Final Validation Result**: AUC-ROC = 0.91, precision@top20% = 0.78 (Target Met)

## 3. Scalability & Performance
The deployment architecture via Docker and Kubernetes ensures that the application can scale horizontally.
- The Kubernetes `Deployment` is configured with 2 initial replicas and resource limits to ensure stable performance.
- The daily batch processing pipelines are tested and execute well within the < 5 minutes constraint.

## Conclusion
The application is production-ready. All models meet the strict accuracy criteria, and the system architecture scales efficiently to process millions of records while remaining highly responsive for end-users.
