import os
import yaml
import json
from datetime import datetime
from google.cloud import storage
from google.oauth2 import service_account
from googleapiclient.discovery import build

def load_config():
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def get_storage_client():
    """Initialize and return Storage client"""
    return storage.Client()

def load_data_from_storage(client, filename):
    """Load data from Google Cloud Storage"""
    config = load_config()
    bucket = client.bucket(config['gcp']['project_id'])
    blob = bucket.blob(f'covid19_data/{filename}')
    
    return json.loads(blob.download_as_string())

def get_datastudio_client():
    """Initialize and return Data Studio client"""
    config = load_config()
    credentials = service_account.Credentials.from_service_account_file(
        'service-account.json',
        scopes=['https://www.googleapis.com/auth/datastudio']
    )
    
    return build('datastudio', 'v1', credentials=credentials)

def update_dashboard():
    """Update Data Studio dashboard with latest data"""
    try:
        config = load_config()
        storage_client = get_storage_client()
        
        # Load latest data
        global_trends = load_data_from_storage(storage_client, 'global_trends.json')
        country_analysis = load_data_from_storage(storage_client, 'country_analysis.json')
        daily_stats = load_data_from_storage(storage_client, 'daily_stats.json')
        
        # Initialize Data Studio client
        datastudio = get_datastudio_client()
        
        # Update dashboard
        dashboard_id = config['datastudio']['dashboard_id']
        
        # Create update request
        update_request = {
            'dataSource': {
                'type': 'BIGQUERY',
                'projectId': config['gcp']['project_id'],
                'datasetId': config['gcp']['dataset_id'],
                'tableId': 'covid19_data'
            },
            'refreshSchedule': {
                'refreshInterval': config['datastudio']['refresh_interval']
            }
        }
        
        # Execute update
        datastudio.reports().update(
            reportId=dashboard_id,
            body=update_request
        ).execute()
        
        return {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'dashboard_id': dashboard_id
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }

def update_dashboard_cloud_function(event, context):
    """Cloud Function entry point"""
    return update_dashboard()

if __name__ == '__main__':
    # For local testing
    result = update_dashboard()
    print(json.dumps(result, indent=2)) 