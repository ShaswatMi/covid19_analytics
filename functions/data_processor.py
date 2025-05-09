import os
import yaml
import json
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.cloud import storage

def load_config():
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def get_bigquery_client():
    """Initialize and return BigQuery client"""
    return bigquery.Client()

def execute_query(client, query_file):
    """Execute a SQL query from file and return results"""
    with open(query_file, 'r') as f:
        query = f.read()
    
    query_job = client.query(query)
    results = query_job.result()
    
    return [dict(row) for row in results]

def save_to_storage(data, filename):
    """Save data to Google Cloud Storage"""
    config = load_config()
    storage_client = storage.Client()
    bucket = storage_client.bucket(config['gcp']['project_id'])
    blob = bucket.blob(f'covid19_data/{filename}')
    
    blob.upload_from_string(
        json.dumps(data, default=str),
        content_type='application/json'
    )

def process_data(event, context):
    """Cloud Function entry point"""
    try:
        config = load_config()
        client = get_bigquery_client()
        
        # Process global trends
        global_trends = execute_query(client, 'sql/global_trends.sql')
        save_to_storage(global_trends, 'global_trends.json')
        
        # Process country analysis
        country_analysis = execute_query(client, 'sql/country_analysis.sql')
        save_to_storage(country_analysis, 'country_analysis.json')
        
        # Process daily stats
        daily_stats = execute_query(client, 'sql/daily_stats.sql')
        save_to_storage(daily_stats, 'daily_stats.json')
        
        return {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'files_processed': [
                'global_trends.json',
                'country_analysis.json',
                'daily_stats.json'
            ]
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }

if __name__ == '__main__':
    # For local testing
    result = process_data(None, None)
    print(json.dumps(result, indent=2)) 