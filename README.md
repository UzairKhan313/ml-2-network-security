# ML-02 ML Network Security — Phishing Detection System

A production-ready **end-to-end Machine Learning pipeline** for network security, specifically designed to detect phishing URLs. The system covers the full ML lifecycle: data ingestion from MongoDB, validation, transformation, model training, experiment tracking with MLflow, serving predictions via a FastAPI REST API, and cloud deployment on AWS (ECR + EC2) with a fully automated CI/CD pipeline.

---

## 📑 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
  - [1. Push Data to MongoDB](#1-push-data-to-mongodb)
  - [2. Run the Training Pipeline](#2-run-the-training-pipeline)
  - [3. Start the FastAPI Server](#3-start-the-fastapi-server)
  - [4. Run via Docker](#4-run-via-docker)
- [API Endpoints](#api-endpoints)
- [CI/CD Pipeline (AWS)](#cicd-pipeline-aws)
- [MLflow Experiment Tracking](#mlflow-experiment-tracking)
- [GitHub Actions Secrets](#github-actions-secrets)

---

## Overview

This project builds a phishing detection ML system using network/URL features. The pipeline:

1. **Ingests** raw phishing data from a MongoDB Atlas collection
2. **Validates** the data schema and checks for data drift
3. **Transforms** features using KNN imputation and preprocessing
4. **Trains** a classification model and evaluates it against quality thresholds
5. **Serves** predictions through a FastAPI web application
6. **Deploys** automatically to AWS EC2 via GitHub Actions on every push to `main`

---

## Architecture

```
MongoDB Atlas
     │
     ▼
Data Ingestion ──► Data Validation ──► Data Transformation ──► Model Trainer
                                                                     │
                                                              MLflow Tracking
                                                                     │
                                                           final_model/ (pkl files)
                                                                     │
                                                            FastAPI Application
                                                                     │
                                                        /train  ──  /predict
                                                                     │
                                                              AWS S3 (artifact sync)
```

---

## Project Structure

```
ml-2-network-security/
├── app.py                        # FastAPI application entry point
├── main.py                       # Standalone training pipeline runner
├── push_data.py                  # Script to upload CSV data to MongoDB
├── setup.py                      # Package installation configuration
├── requirements.txt              # Python dependencies
├── dockerfile                    # Docker image definition
├── .env                          # Local environment variables (not committed)
├── .github/
│   └── workflows/
│       └── main.yml              # GitHub Actions CI/CD pipeline
├── networksecurity/
│   ├── components/
│   │   ├── data_ingestion.py     # Fetches data from MongoDB
│   │   ├── data_validation.py    # Schema checks & drift detection
│   │   ├── data_transformation.py# KNN imputation & preprocessing
│   │   └── model_trainer.py      # Model training & evaluation
│   ├── pipelines/
│   │   └── training_pipeline.py  # Orchestrates all pipeline steps
│   ├── entity/
│   │   ├── config_entity.py      # Dataclass configs for each component
│   │   └── artifacts_entity.py   # Dataclass artifacts (outputs)
│   ├── constant/
│   │   └── training_pipeline/    # All pipeline constants & hyperparameters
│   ├── utils/
│   │   ├── main_utils/           # General utilities (load/save objects)
│   │   └── ml_utils/             # ML-specific utils & model estimator
│   ├── cloud/
│   │   └── s3_syncer.py          # AWS S3 sync helper
│   ├── exception/
│   │   └── exception.py          # Custom exception handler
│   └── logging/
│       └── logger.py             # Centralized logger
├── Network_Data/
│   └── phisingData.csv           # Raw dataset
├── data_schema/
│   └── schema.yaml               # Feature schema for validation
├── Artifacts/                    # Pipeline run artifacts (auto-generated)
├── final_model/                  # Trained model & preprocessor (auto-generated)
│   ├── model.pkl
│   └── preprocessor.pkl
├── prediction_output/            # CSV output of batch predictions
├── templates/
│   └── table.html                # HTML template for prediction results
├── notebooks/                    # Exploratory notebooks
└── logs/                         # Application logs
```

---

## Tech Stack

| Layer               | Technology                         |
| ------------------- | ---------------------------------- |
| Language            | Python 3.10                        |
| ML Framework        | Scikit-learn                       |
| Experiment Tracking | MLflow                             |
| API Framework       | FastAPI + Uvicorn                  |
| Database            | MongoDB Atlas (via PyMongo)        |
| Cloud Storage       | AWS S3                             |
| Containerization    | Docker                             |
| CI/CD               | GitHub Actions → AWS ECR → AWS EC2 |
| Data Processing     | Pandas, NumPy                      |

---

## Prerequisites

- Python **3.10** or later
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/) (for containerized deployment)
- A **MongoDB Atlas** account with a cluster
- An **AWS account** (for S3 and CI/CD deployment)
- AWS CLI installed and configured (for S3 sync)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/UzairKhan313/ml-2-network-security.git
cd ml-2-network-security
```

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This also installs the `networksecurity` package in editable mode via `setup.py`.

> **Note:** If you see `## -e .` at the bottom of `requirements.txt`, run the following to install the local package:
>
> ```bash
> pip install -e .
> ```

---

## Environment Variables

Create a `.env` file in the **project root** before running anything. The app will not connect to MongoDB or AWS without these variables.

```env
# ─── MongoDB Atlas ───────────────────────────────────────────────────────────
# Used by push_data.py to upload the dataset
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority

# Used by app.py (FastAPI) to read data for training
MONGODB_URL_KEY=mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority

# ─── AWS (optional – required for S3 artifact sync) ──────────────────────────
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=us-east-1
```

| Variable                | Required          | Description                                                    |
| ----------------------- | ----------------- | -------------------------------------------------------------- |
| `MONGODB_URI`           | ✅ Yes            | Connection string used by `push_data.py` to insert raw data    |
| `MONGODB_URL_KEY`       | ✅ Yes            | Connection string used by the FastAPI app for training/serving |
| `AWS_ACCESS_KEY_ID`     | ⚠️ For deployment | AWS credentials for S3 sync and ECR deployment                 |
| `AWS_SECRET_ACCESS_KEY` | ⚠️ For deployment | AWS secret key                                                 |
| `AWS_REGION`            | ⚠️ For deployment | AWS region (e.g., `us-east-1`)                                 |

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

---

## Usage

### 1. Push Data to MongoDB

Upload the phishing dataset CSV from `Network_Data/phisingData.csv` to your MongoDB Atlas cluster:

```bash
python push_data.py
```

This inserts all records into the `network_security.Network_data` collection.

---

### 2. Run the Training Pipeline

Execute the full ML pipeline (ingestion → validation → transformation → training):

```bash
python main.py
```

Artifacts are saved under `Artifacts/` and the final model is saved to `final_model/`.

---

### 3. Start the FastAPI Server

```bash
python app.py
```

Or use Uvicorn directly:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: **http://localhost:8000**  
Interactive Swagger docs: **http://localhost:8000/docs**

---

### 4. Run via Docker

```bash
# Build the image
docker build -t network-security .

# Run the container
docker run -d -p 8000:8000 \
  -e MONGODB_URL_KEY="your_mongodb_uri" \
  -e AWS_ACCESS_KEY_ID="your_key" \
  -e AWS_SECRET_ACCESS_KEY="your_secret" \
  -e AWS_REGION="us-east-1" \
  --name networksecurity \
  network-security
```

---

## API Endpoints

| Method | Endpoint   | Description                                        |
| ------ | ---------- | -------------------------------------------------- |
| `GET`  | `/`        | Redirects to `/docs` (Swagger UI)                  |
| `GET`  | `/train`   | Triggers the full training pipeline                |
| `POST` | `/predict` | Upload a CSV file and receive phishing predictions |

### Example: Predict via cURL

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -F "file=@path/to/your/data.csv"
```

The response is an HTML table rendered with prediction results. The output is also saved to `prediction_output/output.csv`.

---

## CI/CD Pipeline (AWS)

The project includes a three-stage GitHub Actions workflow (`.github/workflows/main.yml`) that triggers on every push to the `main` branch:

```
Push to main
     │
     ▼
┌─────────────────────────┐
│  1. CI – Integration    │  Lint & unit test checks
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  2. CD – Build & Push   │  Docker build → push image to Amazon ECR
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  3. CD – Deploy to EC2  │  Pull latest ECR image → run on self-hosted runner
└─────────────────────────┘
```

### GitHub Actions Secrets

The following secrets must be configured in your GitHub repository under **Settings → Secrets and variables → Actions**:

| Secret                  | Description                                                         |
| ----------------------- | ------------------------------------------------------------------- |
| `AWS_ACCESS_KEY_ID`     | AWS IAM user access key                                             |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM user secret key                                             |
| `AWS_REGION`            | AWS region (e.g., `us-east-1`)                                      |
| `ECR_REPOSITORY_NAME`   | Name of the ECR repository                                          |
| `AWS_ECR_LOGIN_URI`     | ECR login URI (e.g., `<account-id>.dkr.ecr.<region>.amazonaws.com`) |

> The self-hosted runner for the deployment step must be configured on your EC2 instance with Docker installed and GitHub Actions runner set up.

---

## MLflow Experiment Tracking

MLflow is used to log metrics and parameters during model training. The tracking database is stored locally in `mlflow.db` and runs are stored in `mlruns/`.

To launch the MLflow UI:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Open **http://localhost:5000** to view all experiment runs, metrics, and model artifacts.

---

## 📄 License

This project was developed by **Uzair Khan** as part of an ML engineering learning project.  
Contact: uzairkhaan2003@gmail.com
