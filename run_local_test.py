import os
import json
import yaml
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config():
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def setup_environment():
    """Set up environment variables for GCP authentication"""
    config = load_config()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config['gcp']['credentials_file']
    logger.info(f"Set GOOGLE_APPLICATION_CREDENTIALS to {config['gcp']['credentials_file']}")
    
    # Set project ID
    os.environ["GCP_PROJECT"] = config['gcp']['project_id']
    logger.info(f"Set GCP_PROJECT to {config['gcp']['project_id']}")

def mock_bigquery_queries():
    """Create mock data instead of running actual BigQuery queries"""
    logger.info("Creating mock data (simulating BigQuery queries)")
    
    # Mock global trends data
    global_trends = []
    for i in range(30):
        global_trends.append({
            "date": (datetime.now().date().replace(day=1) - timedelta(days=i)).isoformat(),
            "global_new_cases": 100000 - i * 1000,
            "global_new_deaths": 2000 - i * 50,
            "global_new_recovered": 80000 - i * 800,
            "global_total_cases": 10000000 + i * 100000,
            "global_total_deaths": 500000 + i * 2000,
            "global_total_recovered": 9000000 + i * 90000,
            "cases_7d_avg": 95000 - i * 900,
            "deaths_7d_avg": 1900 - i * 45,
            "recovered_7d_avg": 75000 - i * 750,
            "case_fatality_rate": 2.0,
            "recovery_rate": 80.0
        })
    
    # Mock country analysis data
    countries = ["United States", "India", "Brazil", "United Kingdom", "Germany"]
    country_analysis = []
    for i, country in enumerate(countries):
        country_analysis.append({
            "country_name": country,
            "latest_date": datetime.now().date().isoformat(),
            "total_new_cases_30d": 1000000 - i * 200000,
            "total_new_deaths_30d": 20000 - i * 4000,
            "total_new_recovered_30d": 800000 - i * 160000,
            "total_cases": 10000000 - i * 1000000,
            "total_deaths": 200000 - i * 20000,
            "total_recovered": 9000000 - i * 900000,
            "population": 100000000 - i * 10000000,
            "cases_per_100k": 10000 - i * 1000,
            "deaths_per_100k": 200 - i * 20,
            "case_fatality_rate": 2.0,
            "recovery_rate": 90.0
        })
    
    # Mock daily stats
    daily_stats = []
    for i in range(7):
        daily_stats.append({
            "date": (datetime.now().date() - timedelta(days=i)).isoformat(),
            "countries_with_cases": 200,
            "total_new_cases": 500000 - i * 20000,
            "total_new_deaths": 10000 - i * 400,
            "total_new_recovered": 400000 - i * 16000,
            "total_cases": 100000000 + i * 500000,
            "total_deaths": 2000000 + i * 10000,
            "total_recovered": 90000000 + i * 400000,
            "global_new_cases_per_100k": 6.5 - i * 0.2,
            "global_new_deaths_per_100k": 0.13 - i * 0.005,
            "global_case_fatality_rate": 2.0,
            "global_recovery_rate": 80.0,
            "top_10_countries": [
                {
                    "country_name": countries[0],
                    "new_confirmed": 100000 - i * 5000,
                    "new_deceased": 2000 - i * 100,
                    "new_recovered": 80000 - i * 4000,
                    "new_cases_per_100k": 30.0 - i * 1.5,
                    "new_deaths_per_100k": 0.6 - i * 0.03
                },
                {
                    "country_name": countries[1],
                    "new_confirmed": 90000 - i * 4500,
                    "new_deceased": 1800 - i * 90,
                    "new_recovered": 72000 - i * 3600,
                    "new_cases_per_100k": 27.0 - i * 1.35,
                    "new_deaths_per_100k": 0.54 - i * 0.027
                }
            ]
        })
    
    return global_trends, country_analysis, daily_stats

def save_mock_data(global_trends, country_analysis, daily_stats):
    """Save mock data to JSON files"""
    os.makedirs("mock_data", exist_ok=True)
    
    with open("mock_data/global_trends.json", "w") as f:
        json.dump(global_trends, f, indent=2, default=str)
    logger.info("Saved mock global trends data")
    
    with open("mock_data/country_analysis.json", "w") as f:
        json.dump(country_analysis, f, indent=2, default=str)
    logger.info("Saved mock country analysis data")
    
    with open("mock_data/daily_stats.json", "w") as f:
        json.dump(daily_stats, f, indent=2, default=str)
    logger.info("Saved mock daily stats data")

def simulate_dashboard():
    """Simulate creating a dashboard"""
    logger.info("Simulating dashboard creation")
    
    # Create mock dashboard definition
    dashboard = {
        "name": "COVID-19 Analytics Dashboard",
        "type": "DASHBOARD",
        "dashboardType": "EXPLORATION",
        "dateRangeSelection": {
            "includeToday": True,
            "relativePresets": ["LAST_30_DAYS", "LAST_90_DAYS", "LAST_YEAR"]
        },
        "refreshSchedule": {
            "refreshInterval": 3600  # seconds
        },
        "sections": [
            {
                "name": "Global Trends",
                "position": {"x": 0, "y": 0, "width": 12, "height": 6},
                "components": [
                    {
                        "name": "Global Cases and Deaths",
                        "type": "LINE_CHART",
                        "dimensions": ["date"],
                        "metrics": ["global_new_cases", "global_new_deaths", "cases_7d_avg", "deaths_7d_avg"]
                    }
                ]
            },
            {
                "name": "Country Analysis",
                "position": {"x": 0, "y": 6, "width": 12, "height": 6},
                "components": [
                    {
                        "name": "Top Countries",
                        "type": "BAR_CHART",
                        "dimensions": ["country_name"],
                        "metrics": ["total_cases", "total_deaths", "cases_per_100k"]
                    }
                ]
            },
            {
                "name": "Daily Statistics",
                "position": {"x": 0, "y": 12, "width": 12, "height": 6},
                "components": [
                    {
                        "name": "Daily New Cases",
                        "type": "LINE_CHART",
                        "dimensions": ["date"],
                        "metrics": ["total_new_cases", "total_new_deaths"]
                    }
                ]
            }
        ]
    }
    
    # Save mock dashboard
    os.makedirs("dashboard", exist_ok=True)
    with open("dashboard/covid19_dashboard.json", "w") as f:
        json.dump(dashboard, f, indent=2)
    
    logger.info("Dashboard configuration saved to dashboard/covid19_dashboard.json")
    
    # Generate dashboard URL (mock)
    dashboard_url = "https://datastudio.google.com/reporting/mock-dashboard-id/page/1"
    
    return dashboard_url

def main():
    """Main function to run local test"""
    logger.info("Starting local test of COVID-19 Analytics Project")
    
    # Setup environment
    setup_environment()
    
    # Generate mock data
    logger.info("Generating mock data (simulating BigQuery queries)")
    global_trends, country_analysis, daily_stats = mock_bigquery_queries()
    
    # Save mock data
    save_mock_data(global_trends, country_analysis, daily_stats)
    
    # Simulate dashboard creation
    dashboard_url = simulate_dashboard()
    
    # Display summary
    print("\n" + "="*80)
    print("COVID-19 ANALYTICS PROJECT - LOCAL TEST SUMMARY")
    print("="*80)
    print(f"Project ID: {os.environ.get('GCP_PROJECT')}")
    print(f"Credentials: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')}")
    print("\nMock Data Files Generated:")
    print("  - mock_data/global_trends.json")
    print("  - mock_data/country_analysis.json")
    print("  - mock_data/daily_stats.json")
    print("\nDashboard Configuration:")
    print("  - dashboard/covid19_dashboard.json")
    print(f"\nMock Dashboard URL: {dashboard_url}")
    print("\nNOTE: This is a local test with mock data. To access the real dashboard,")
    print("      deploy the project to Google Cloud Platform and set up Data Studio.")
    print("="*80)
    
    logger.info("Local test completed successfully")

if __name__ == "__main__":
    main() 