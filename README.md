README.md for Kubeflow Healthcare Project

# Kubeflow Healthcare ML Pipeline on Google Cloud

This repository contains an example Kubeflow pipeline for processing  healthcare data, training a machine learning model, and evaluating its performance on Google Kubernetes Engine (GKE) with CI/CD integration using Google Cloud Build.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup Guide](#setup-guide)
  - [1. Google Cloud Project Setup](#1-google-cloud-project-setup)
  - [2. GKE Cluster Creation](#2-gke-cluster-creation)
  - [3. Kubeflow Installation](#3-kubeflow-installation)
  - [4. GitHub Repository and CI/CD](#4-github-repository-and-cicd)
  - [5. Run the Pipeline](#5-run-the-pipeline)
- [Observability](#observability)
- [Testing and Validation](#testing-and-validation)
- [ Healthcare Data](#-healthcare-data)
- [Cleanup](#cleanup)

## Project Overview

This project demonstrates an end-to-end MLOps workflow on GCP using Kubeflow. The key stages include:
- Data Ingestion (from GCS)
- Data Preprocessing
- Model Training (Random Forest Regressor)
- Model Evaluation
- Automated deployment of the Kubeflow pipeline via Cloud Build.

## Architecture

```mermaid
graph TD
    A[GitHub Push] --> B(Cloud Build Trigger);
    B --> C{Cloud Build Pipeline};
    C --> D[Compile KFP Pipeline];
    C --> F[Deploy KFP Pipeline to GKE];
    F --> G(Kubeflow Pipelines on GKE);
    G --> H[Run Pipeline (UI/SDK)];
    H --> I[GCS (Input/Output Data/Artifacts)];
    I --> J[Cloud Logging];
    I --> K[Cloud Monitoring];
    J & K --> L[Google Cloud Observability Dashboard];
    H --> M[Kubeflow UI];
Prerequisites
Before starting, ensure you have:

A Google Cloud Platform account with billing enabled.

Google Cloud CLI (gcloud) installed and configured on your MacBook.

kubectl installed.

git installed.

A GitHub account.

Docker Desktop for Mac installed and running.

kustomize installed (brew install kustomize).

Setup Guide
Follow these steps to set up the project from scratch.

1. Google Cloud Project Setup
Bash

# Set your project ID
export PROJECT_ID="your-kubeflow-healthcare-project" # Replace with your project ID
gcloud config set project $PROJECT_ID

# Enable necessary APIs
gcloud services enable \
    container.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    cloudresourcemanager.googleapis.com \
    compute.googleapis.com \
    iam.googleapis.com \
    logging.googleapis.com \
    monitoring.googleapis.com \
    stackdriver.googleapis.com
2. GKE Cluster Creation
Bash

export REGION="us-central1" # Or your preferred region
export ZONE="${REGION}-a"   # Or your preferred zone

export CLUSTER_NAME="kubeflow-healthcare-cluster"

gcloud container clusters create $CLUSTER_NAME \
    --zone $ZONE \
    --machine-type "e2-standard-4" \
    --num-nodes "3" \
    --scopes "cloud-platform" \
    --enable-stackdriver-kubernetes \
    --enable-ip-alias \
    --project $PROJECT_ID

gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE --project $PROJECT_ID
3. Kubeflow Installation
Bash

# Ensure kustomize is installed: brew install kustomize
git clone [https://github.com/kubeflow/manifests.git](https://github.com/kubeflow/manifests.git)
cd manifests
git checkout v1.8.0 # Or latest stable release
while ! kustomize build example/gcp | kubectl apply -f -; do echo "Retrying to apply Kubeflow manifests..."; sleep 10; done

kubectl get pods -n kubeflow -w
kubectl get services -n istio-system istio-ingressgateway
# Access Kubeflow UI at http://<EXTERNAL-IP>
4. GitHub Repository and CI/CD
Create a GitHub Repository:
Create a public GitHub repository (e.g., kubeflow-healthcare-pipeline).

Bash

git clone [https://github.com/YOUR_GITHUB_USERNAME/kubeflow-healthcare-pipeline.git](https://github.com/YOUR_GITHUB_USERNAME/kubeflow-healthcare-pipeline.git)
cd kubeflow-healthcare-pipeline
Add Data:
Create data/healthcare_data.csv in your repository with the data provided in the guide.

Add Kubeflow Pipeline Code:
Create pipeline.py and cloudbuild.yaml in the root of your repository (content as provided in the guidance above).

Set up Cloud Build Trigger:
In GCP Console -> Cloud Build -> Triggers:

Name: kubeflow-pipeline-ci-cd

Event: Push to a branch

Source: Link to your GitHub repo, branch ^main$

Configuration: cloudbuild.yaml

Substitutions:

_PROJECT_ID: your-kubeflow-healthcare-project

_CLUSTER_NAME: kubeflow-healthcare-cluster

_ZONE: us-central1-a

Push Code:

Bash

git add .
git commit -m "Initial Kubeflow pipeline setup with CI/CD"
git push origin main
5. Run the Pipeline
Upload  Data to GCS:

Bash

gsutil mb -l ${REGION} gs://${PROJECT_ID}-kubeflow-data/
gsutil cp data/healthcare_data.csv gs://${PROJECT_ID}-kubeflow-data/raw/healthcare_data.csv
Access Kubeflow UI: Go to http://<EXTERNAL-IP> (from istio-ingressgateway service).

Create a Run:

Navigate to Pipelines.

Select Healthcare Data ML Pipeline.

Click Create run.

Run name: healthcare-run-1

Experiment: Create Healthcare ML Experiments.

Parameters: Set data_input_gcs_uri to gs://your-kubeflow-healthcare-project-kubeflow-data/raw/healthcare_data.csv.

Click Start.

Observability
Monitor your pipeline runs using Google Cloud Observability:

Cloud Logging: View component logs (e.g., data processing messages, model training status) in Logs Explorer. Filter by Kubernetes resource type, cluster, and namespace.

Cloud Monitoring: Create custom dashboards in Metrics Explorer to track CPU, memory, and network usage of your Kubeflow pods on GKE.

Kubeflow UI: Provides real-time status, step-by-step progress, and artifact visualization for each pipeline run.

Testing and Validation
Pipeline Execution: Verify that all pipeline steps complete successfully in the Kubeflow UI.

Output Artifacts: Download the processed_data.csv, model.pkl, and metrics.json from the Kubeflow UI for specific runs and inspect their content. Check the mse and r2_score in metrics.json to understand model performance.

Healthcare Data
The data/healthcare_data.csv contains a small sample of synthetic healthcare data used for demonstration purposes.
