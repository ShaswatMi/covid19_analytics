# COVID-19 Analytics Project Deployment Guide

This guide outlines the steps to deploy the COVID-19 Analytics project to Google Cloud Platform.

## Prerequisites

1. Google Cloud Platform account
2. Billing enabled on your GCP account
3. Google Cloud SDK installed locally

## Step 1: Set Up GCP Project

1. Create a new GCP project:
   ```bash
   gcloud projects create covid-19-analytics --name="COVID-19 Analytics"
   ```

2. Set the project as your default:
   ```bash
   gcloud config set project covid-19-analytics
   ```

3. Enable required APIs:
   ```bash
   gcloud services enable bigquery.googleapis.com
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable storage.googleapis.com
   ```

## Step 2: Create Service Account

1. Create a service account:
   ```bash
   gcloud iam service-accounts create covid19-service-account \
     --display-name="COVID-19 Analytics Service Account"
   ```

2. Grant necessary permissions:
   ```bash
   gcloud projects add-iam-policy-binding covid-19-analytics \
     --member="serviceAccount:covid19-service-account@covid-19-analytics.iam.gserviceaccount.com" \
     --role="roles/bigquery.admin"
   
   gcloud projects add-iam-policy-binding covid-19-analytics \
     --member="serviceAccount:covid19-service-account@covid-19-analytics.iam.gserviceaccount.com" \
     --role="roles/storage.admin"
   ```

3. Create and download a key:
   ```bash
   gcloud iam service-accounts keys create service-account.json \
     --iam-account=covid19-service-account@covid-19-analytics.iam.gserviceaccount.com
   ```

## Step 3: Create Cloud Storage Bucket

1. Create a GCS bucket:
   ```bash
   gsutil mb -l us-central1 gs://covid-19-analytics-data
   ```

## Step 4: Create BigQuery Dataset

1. Create a BigQuery dataset:
   ```bash
   bq mk --location=US covid19_data
   ```

## Step 5: Deploy Cloud Functions

1. Create a Cloud Storage bucket for functions:
   ```bash
   gsutil mb -l us-central1 gs://covid-19-analytics-functions
   ```

2. Deploy the data processor function:
   ```bash
   gcloud functions deploy covid19-data-processor \
     --runtime python39 \
     --trigger-http \
     --entry-point process_data \
     --source functions/ \
     --memory 256MB \
     --timeout 540s \
     --service-account covid19-service-account@covid-19-analytics.iam.gserviceaccount.com
   ```

3. Deploy the dashboard updater function:
   ```bash
   gcloud functions deploy covid19-dashboard-updater \
     --runtime python39 \
     --trigger-http \
     --entry-point update_dashboard_cloud_function \
     --source functions/ \
     --memory 256MB \
     --timeout 540s \
     --service-account covid19-service-account@covid-19-analytics.iam.gserviceaccount.com
   ```

## Step 6: Set Up Cloud Scheduler

1. Create a scheduler job for the data processor:
   ```bash
   gcloud scheduler jobs create http covid19-data-processor-daily \
     --schedule="0 0 * * *" \
     --uri="https://us-central1-covid-19-analytics.cloudfunctions.net/covid19-data-processor" \
     --oidc-service-account-email="covid19-service-account@covid-19-analytics.iam.gserviceaccount.com" \
     --oidc-token-audience="https://us-central1-covid-19-analytics.cloudfunctions.net/covid19-data-processor"
   ```

2. Create a scheduler job for the dashboard updater:
   ```bash
   gcloud scheduler jobs create http covid19-dashboard-updater-hourly \
     --schedule="0 * * * *" \
     --uri="https://us-central1-covid-19-analytics.cloudfunctions.net/covid19-dashboard-updater" \
     --oidc-service-account-email="covid19-service-account@covid-19-analytics.iam.gserviceaccount.com" \
     --oidc-token-audience="https://us-central1-covid-19-analytics.cloudfunctions.net/covid19-dashboard-updater"
   ```

## Step 7: Set Up Google Data Studio Dashboard

1. Go to [Google Data Studio](https://datastudio.google.com/)
2. Create a new report
3. Connect to your BigQuery data sources:
   - Add BigQuery as a data source
   - Select the `covid19_data` dataset
   - Create connections for the various tables/views
4. Build your dashboard using the template provided in `dashboard/covid19_dashboard.json` as a reference
5. Configure automatic refresh settings
6. Share the dashboard with stakeholders

## Step 8: Update Configuration

1. Update the `config.yaml` file with your GCP project details:
   - Project ID
   - Credentials file path
   - Dashboard ID

## Monitoring and Maintenance

1. Monitor Cloud Function logs:
   ```bash
   gcloud functions logs read covid19-data-processor
   gcloud functions logs read covid19-dashboard-updater
   ```

2. Check Cloud Scheduler job execution:
   ```bash
   gcloud scheduler jobs list
   ```

3. Review BigQuery usage and quotas in GCP Console

## Troubleshooting

1. If Cloud Functions fail:
   - Check logs for errors
   - Verify service account permissions
   - Ensure billing is enabled

2. If data is not updating:
   - Check Cloud Scheduler jobs
   - Verify BigQuery permissions
   - Check storage bucket access

3. If dashboard is not refreshing:
   - Verify Data Studio connection settings
   - Check refresh interval configuration
   - Ensure data sources are accessible 