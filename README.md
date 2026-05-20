# Customer Churn Prediction System

A complete end-to-end machine learning project that predicts whether a telecom customer will churn (leave the company). It includes data pipelines, model training, a REST API, an interactive dashboard, business rules for retention, and Jupyter notebooks for exploration.

**Dataset:** Telco Customer Churn (Kaggle) — ~7,000 customers with demographics, services, billing, and churn labels.

**Model performance (typical run):**
- Accuracy: ~78%
- ROC-AUC: ~84%

---

## Table of Contents

1. [What This Project Does](#what-this-project-does)
2. [System Architecture](#system-architecture)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [How to Run Everything](#how-to-run-everything)
7. [Module-by-Module Explanation](#module-by-module-explanation)
8. [API Documentation](#api-documentation)
9. [Dashboard Guide](#dashboard-guide)
10. [Jupyter Notebooks](#jupyter-notebooks)
11. [Configuration](#configuration)
12. [Database Schema](#database-schema)
13. [Business Logic](#business-logic)
14. [Deployment](#deployment)
15. [Troubleshooting](#troubleshooting)

---

## What This Project Does

| Stage | What happens |
|-------|----------------|
| **Extract** | Loads raw CSV from `1_data/raw/telco_churn.csv` |
| **Transform** | Cleans data, fixes types, engineers features |
| **Load** | Saves cleaned data to CSV and SQLite database |
| **Train** | Trains a Random Forest classifier, saves model + encoders |
| **Predict** | Scores customers for churn probability and risk level |
| **Serve** | Exposes predictions via FastAPI and Streamlit dashboard |
| **Act** | Suggests retention actions (discounts, calls, surveys) |

---

## System Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Raw CSV Data   │────▶│   ETL Pipeline   │────▶│  SQLite DB +    │
│  (Kaggle)       │     │  extract/transform│     │  cleaned CSV    │
└─────────────────┘     └────────┬─────────┘     └────────┬────────┘
                                 │                        │
                                 ▼                        ▼
                        ┌──────────────────┐     ┌─────────────────┐
                        │ Feature Eng.     │────▶│  Random Forest  │
                        │ encode + scale   │     │  Model (.pkl)   │
                        └──────────────────┘     └────────┬────────┘
                                                          │
                    ┌─────────────────────────────────────┼─────────────────────────────────────┐
                    ▼                                     ▼                                     ▼
           ┌────────────────┐                   ┌────────────────┐                   ┌────────────────┐
           │  FastAPI       │                   │  Streamlit     │                   │  Jupyter         │
           │  /api/v1/...   │                   │  Dashboard     │                   │  Notebooks       │
           └────────────────┘                   └────────────────┘                   └────────────────┘
```

**Data flow:**
1. Raw telco data → ETL cleans and enriches it
2. Feature engineering prepares columns for ML
3. Model learns patterns (who churns vs stays)
4. API and dashboard serve predictions to users
5. Business rules recommend retention actions for high-risk customers

---

## Project Structure

```
customer-churn-system/
│
├── 1_data/
│   ├── raw/telco_churn.csv          # Original Kaggle dataset
│   └── processed/cleaned_churn.csv  # Output after ETL
│
├── 2_notebooks/                     # Jupyter notebooks (EDA → evaluation)
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_model_building.ipynb
│   └── 04_evaluation.ipynb
│
├── 3_etl_pipeline/                  # Extract, Transform, Load
│   ├── extract.py                   # Read CSV
│   ├── transform.py                 # Clean + feature engineering
│   ├── load.py                      # Write to SQLite
│   └── pipeline_runner.py           # Run full ETL
│
├── 4_feature_engineering/
│   ├── features.py                  # Create ML features
│   ├── encoding.py                  # Label encoding for categories
│   └── scaling.py                   # StandardScaler for numerics
│
├── 5_model/
│   ├── train.py                     # Train Random Forest
│   ├── predict.py                   # Single/batch predictions
│   ├── churn_model.pkl              # Saved model (after training)
│   ├── encoders.pkl                 # Saved label encoders
│   ├── scaler.pkl                   # Saved scaler
│   └── model_metrics.json           # Accuracy, ROC-AUC
│
├── 6_api/                           # FastAPI REST API
│   ├── app.py                       # App entry + CORS
│   ├── routes.py                    # Endpoints
│   ├── schemas.py                   # Pydantic models (Swagger docs)
│   └── utils.py                     # Validation helpers
│
├── 7_dashboard/                     # Streamlit UI
│   ├── streamlit_app.py             # Main app + navigation
│   └── pages/
│       ├── overview.py              # KPIs + churn chart
│       ├── prediction.py            # Manual churn prediction form
│       └── analytics.py             # Risk segments + charts
│
├── 8_database/
│   ├── schema.sql                   # Table definitions
│   ├── db_connect.py                # SQLite connection
│   └── insert_data.py               # Store batch predictions
│
├── 9_business_logic/
│   ├── churn_rules.py               # Retention actions (discount, call, etc.)
│   └── risk_segmentation.py         # High / Medium / Low risk
│
├── 10_ab_testing/
│   ├── experiment_design.py         # A/B test variant assignment
│   └── metrics_tracking.py          # Conversion event logging
│
├── 11_reports/
│   ├── generate_charts.py           # Save PNG charts
│   └── charts/                      # Generated images
│
├── 12_config/
│   └── config.py                    # Paths, thresholds, constants
│
├── 13_deployment/
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Container for API
│   ├── render.yaml                  # Render.com deploy config
│   └── aws.yaml                     # AWS deploy reference
│
├── 14_logs/
│   ├── pipeline.log                 # ETL logs
│   └── api.log                      # API request logs
│
├── main.py                          # Main entry: pipeline + CLI flags
├── run_api.py                       # Start FastAPI only
├── run_dashboard.py                 # Start Streamlit only
├── run_notebooks.py                 # Start Jupyter only
└── README.md                        # This file
```

---

## Prerequisites

- **Python 3.10+** (tested on Python 3.11 / 3.14)
- **pip** (Python package manager)
- **Web browser** (Chrome, Edge, Firefox) for API docs, dashboard, and Jupyter
- **Optional:** Docker (for containerized deployment)

---

## Installation

Open PowerShell or Command Prompt and run:

```powershell
cd "e:\real project\customer-churn-system"
pip install -r 13_deployment/requirements.txt
```

This installs: `pandas`, `numpy`, `scikit-learn`, `fastapi`, `uvicorn`, `streamlit`, `matplotlib`, `seaborn`, `jupyter`, and related packages.

**Verify installation:**

```powershell
python -c "import pandas, sklearn, fastapi, streamlit; print('OK')"
```

---

## How to Run Everything

### Step 1 — Run the full ML pipeline (do this first)

This processes data, trains the model, and stores sample predictions in the database.

```powershell
cd "e:\real project\customer-churn-system"
python main.py
```

**What runs:**
1. ETL: loads 7,043 rows → saves `cleaned_churn.csv` + `churn.db`
2. Training: saves `churn_model.pkl`, `model_metrics.json`
3. Predictions: inserts 100 predictions into the database

**Expected output:**
```
ETL pipeline complete
Model trained — accuracy: 0.7828, ROC-AUC: 0.8371
Stored 100 predictions in database
Done! Start API: python main.py --api | Dashboard: python main.py --dashboard
```

---

### Step 2 — Run pipeline steps individually (optional)

```powershell
python main.py --etl           # Data cleaning only
python main.py --train         # Train model only
python main.py --predictions   # Batch predict → database
```

---

### Step 3 — Start API and Dashboard (two separate terminals)

You need **two terminal windows** because both servers run continuously.

**Terminal 1 — API (Swagger documentation):**

```powershell
cd "e:\real project\customer-churn-system"
python run_api.py
```

| URL | Purpose |
|-----|---------|
| http://127.0.0.1:8000/docs | Interactive Swagger UI (try endpoints) |
| http://127.0.0.1:8000/redoc | Alternative API documentation |
| http://127.0.0.1:8000/api/v1/health | Health check |

Press **Ctrl+C** to stop the API.

**Terminal 2 — Streamlit dashboard:**

```powershell
cd "e:\real project\customer-churn-system"
python run_dashboard.py
```

Open: **http://localhost:8501**

Press **Ctrl+C** to stop the dashboard.

---

### Step 4 — Jupyter notebooks (optional)

```powershell
python run_notebooks.py
```

Copy the URL from the terminal (includes a `token=...`) and open it in your browser, e.g.:

```
http://localhost:8888/tree?token=...
```

Run notebooks in order: `01` → `02` → `03` → `04`.

---

### Quick command reference

| Goal | Command |
|------|---------|
| Full pipeline | `python main.py` |
| API only | `python run_api.py` |
| Dashboard only | `python run_dashboard.py` |
| Notebooks only | `python run_notebooks.py` |
| Generate charts | `python 11_reports/generate_charts.py` |
| ETL only | `python main.py --etl` |
| Train only | `python main.py --train` |

---

## Module-by-Module Explanation

### `1_data/` — Data storage

| File | Description |
|------|-------------|
| `raw/telco_churn.csv` | Original Kaggle dataset (21 columns, ~7K rows) |
| `processed/cleaned_churn.csv` | Cleaned data after ETL (Churn as 0/1, fixed TotalCharges) |

---

### `3_etl_pipeline/` — ETL pipeline

| File | What it does |
|------|--------------|
| `extract.py` | Reads CSV with pandas |
| `transform.py` | Drops duplicates, fixes `TotalCharges`, maps Yes/No → 1/0, creates `AvgMonthlyCharge`, `HasInternet`, `HasStreaming`, `TenureGroup` |
| `load.py` | Creates SQLite tables and inserts customer records |
| `pipeline_runner.py` | Runs extract → transform → load in sequence |

**Run directly:**
```powershell
python 3_etl_pipeline/pipeline_runner.py
```

---

### `4_feature_engineering/` — ML feature preparation

| File | What it does |
|------|--------------|
| `features.py` | Adds `ContractRisk`, `TenureGroupNum`, `ChargeRatio` |
| `encoding.py` | Label-encodes categorical columns (gender, Contract, etc.) |
| `scaling.py` | StandardScaler on numeric features |

---

### `5_model/` — Machine learning

| File | What it does |
|------|--------------|
| `train.py` | Trains RandomForest (100 trees), 80/20 split, saves model + metrics |
| `predict.py` | Loads model and returns churn probability + risk level |

**Risk levels:**
- **High** — probability ≥ 70%
- **Medium** — probability ≥ 40%
- **Low** — probability < 40%

**Run directly:**
```powershell
python 5_model/train.py
python 5_model/predict.py
```

---

### `6_api/` — REST API (FastAPI)

| File | What it does |
|------|--------------|
| `app.py` | Creates FastAPI app, CORS, redirects `/` → `/docs` |
| `routes.py` | Defines `/health`, `/predict`, `/metrics` |
| `schemas.py` | Pydantic models for request/response (powers Swagger UI) |
| `utils.py` | Validates required customer fields |

---

### `7_dashboard/` — Streamlit web UI

| Page | What it shows |
|------|---------------|
| **Overview** | Total customers, churn rate, avg tenure, model accuracy |
| **Prediction** | Form to enter customer details and get churn prediction |
| **Analytics** | Risk segment distribution, churn by contract, scatter plots |

---

### `8_database/` — SQLite storage

| File | What it does |
|------|--------------|
| `schema.sql` | `customers` and `predictions` tables |
| `db_connect.py` | Connection helper |
| `insert_data.py` | Batch predict and store results |

Database file: `8_database/churn.db` (created after ETL).

---

### `9_business_logic/` — Retention rules

| File | What it does |
|------|--------------|
| `churn_rules.py` | Recommends actions: discount offer, retention call, survey, plan review |
| `risk_segmentation.py` | Groups customers into High / Medium / Low risk |

---

### `10_ab_testing/` — Experiment framework

| File | What it does |
|------|--------------|
| `experiment_design.py` | Assigns customers to control vs treatment (e.g. 20% discount test) |
| `metrics_tracking.py` | Logs conversion events to `experiment_log.jsonl` |

---

### `12_config/config.py` — Central settings

All paths, model settings, API port, and risk thresholds are defined here. Edit this file to change behavior project-wide.

---

## API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Check if API is running |
| POST | `/api/v1/predict` | Predict churn for one customer |
| GET | `/api/v1/metrics` | Return model accuracy and ROC-AUC |

### Example: Predict churn

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/predict" -Method POST -ContentType "application/json" -Body '{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "tenure": 1,
  "PhoneService": "No",
  "MultipleLines": "No phone service",
  "InternetService": "DSL",
  "OnlineSecurity": "No",
  "OnlineBackup": "Yes",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "No",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 29.85,
  "TotalCharges": 29.85
}'
```

**Example response:**
```json
{
  "customer_id": null,
  "churn_probability": 0.5751,
  "will_churn": true,
  "risk_level": "Medium"
}
```

### Interactive docs

Open **http://127.0.0.1:8000/docs** → expand **POST /api/v1/predict** → **Try it out** → **Execute**.

---

## Dashboard Guide

1. Run `python run_dashboard.py`
2. Open **http://localhost:8501**
3. Use the sidebar to switch pages:

| Page | Use case |
|------|----------|
| **Overview** | See dataset stats and model performance |
| **Prediction** | Enter customer details and get instant churn score |
| **Analytics** | Explore risk segments and churn patterns |

**Note:** Run `python main.py` first so the model and processed data exist.

---

## Jupyter Notebooks

| Notebook | Purpose |
|----------|---------|
| `01_data_exploration.ipynb` | EDA — distributions, churn counts |
| `02_data_preprocessing.ipynb` | Run ETL transform interactively |
| `03_model_building.ipynb` | Train model and view metrics |
| `04_evaluation.ipynb` | Review accuracy and ROC-AUC |

**Start Jupyter:**
```powershell
python run_notebooks.py
```

**Important on Windows:** Use `python -m notebook`, not `jupyter notebook` (see Troubleshooting).

In each notebook: **Shift + Enter** to run a cell, or **Run → Run All Cells**.

---

## Configuration

Edit `12_config/config.py` to change:

| Setting | Default | Description |
|---------|---------|-------------|
| `API_HOST` | `127.0.0.1` | API bind address |
| `API_PORT` | `8000` | API port |
| `TEST_SIZE` | `0.2` | Train/test split ratio |
| `RANDOM_STATE` | `42` | Reproducibility seed |
| `HIGH_RISK_THRESHOLD` | `0.7` | High risk cutoff |
| `MEDIUM_RISK_THRESHOLD` | `0.4` | Medium risk cutoff |

---

## Database Schema

**`customers` table** — cleaned customer records from ETL.

**`predictions` table** — model outputs:

| Column | Type | Description |
|--------|------|-------------|
| customerID | TEXT | Customer identifier |
| churn_probability | REAL | 0.0 – 1.0 |
| will_churn | INTEGER | 0 or 1 |
| risk_level | TEXT | High / Medium / Low |
| created_at | TIMESTAMP | When prediction was made |

---

## Business Logic

When a customer is high risk, the API can return retention actions:

| Action | When triggered |
|--------|----------------|
| `immediate_call` | Churn probability ≥ 70% |
| `offer_discount` | High risk + month-to-month contract |
| `send_survey` | Medium risk (40–70%) |
| `onboarding_support` | New customer (< 6 months) at risk |
| `plan_review` | High monthly charges + medium+ risk |

---

## Deployment

### Docker (API only)

```powershell
cd "e:\real project\customer-churn-system"
docker build -f 13_deployment/Dockerfile -t churn-api .
docker run -p 8000:8000 churn-api
```

API will be at http://localhost:8000/docs

### Cloud

- **Render:** Use `13_deployment/render.yaml`
- **AWS:** See `13_deployment/aws.yaml` for reference config

Before deploying, ensure the model is trained (`python main.py`) and include `churn_model.pkl` in the image or train on startup.

---

## Troubleshooting

### `jupyter` is not recognized

**Problem:** `jupyter notebook` fails with "command not found".

**Fix:** Use Python module syntax:
```powershell
python -m notebook 2_notebooks/
# or
python run_notebooks.py
```

Do **not** use `python -m jupyter notebook` — you may get `jupyter-notebook not found`.

---

### `KeyboardInterrupt` traceback when stopping API/dashboard/Jupyter

**Problem:** Long error when pressing Ctrl+C.

**Cause:** Normal — you stopped a running server.

**Fix:** Ignore the traceback, or use `run_api.py` / `run_dashboard.py` / `run_notebooks.py` which handle Ctrl+C cleanly.

---

### API docs not loading / uvicorn not starting

**Problem:** `6_api.app:app` module path fails on some setups.

**Fix:** Use the dedicated launcher:
```powershell
python run_api.py
```
Open **http://127.0.0.1:8000/docs** (not `0.0.0.0`).

---

### Dashboard shows errors on Prediction page

**Problem:** Model files missing.

**Fix:** Train the model first:
```powershell
python main.py --train
```

---

### Notebook "not trusted" warning

**Problem:** Jupyter asks to trust the notebook.

**Fix:** Click **Trust** or **Run** in the Jupyter UI. This is a security feature, not an error.

---

### Port already in use

**Problem:** `Address already in use` on 8000 or 8501.

**Fix:** Stop the other process or change port:
```powershell
python run_api.py --port 8001
python -m streamlit run 7_dashboard/streamlit_app.py --server.port 8502
```

---

## Recommended workflow (first time)

```text
1. pip install -r 13_deployment/requirements.txt
2. python main.py                          # Train everything
3. python run_api.py                       # Terminal 1 — API
4. python run_dashboard.py                 # Terminal 2 — Dashboard
5. python run_notebooks.py                 # Optional — exploration
```

---

## dataset

- **Dataset:** [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) (Kaggle)
- Place raw file at: `1_data/raw/telco_churn.csv`

---

## Support

If something fails:
1. Check you are in the project folder: `cd "e:\real project\customer-churn-system"`
2. Run `python main.py` before API/dashboard
3. Use the URLs exactly: `127.0.0.1` for API, `localhost` for dashboard/Jupyter
4. See [Troubleshooting](#troubleshooting) above
