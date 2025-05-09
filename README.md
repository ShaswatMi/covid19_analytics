# COVID-19 Data Analytics Project

This project performs big data analytics on COVID-19 data using Google Cloud Platform services, specifically BigQuery and Data Studio.

## Project Overview

The project analyzes COVID-19 data to provide insights into global trends, case distributions, and patterns. It uses the following technologies:

- Google BigQuery (Free-tier)
- Google Data Studio (Free)
- Google Cloud Functions
- Python for data processing

## Setup Instructions

1. **Google Cloud Platform Setup**
   - Create a new GCP project
   - Enable BigQuery API
   - Enable Cloud Functions API
   - Set up billing account (required for BigQuery)

2. **Dataset Setup**
   - The project uses the COVID-19 Open Dataset available in BigQuery
   - Dataset location: `bigquery-public-data.covid19_open_data.covid19_open_data`

3. **Local Environment Setup**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**
   - Update `config.yaml` with your GCP project details
   - Set up authentication using service account credentials

## Project Structure

```
covid19_analytics/
├── README.md
├── requirements.txt
├── config.yaml
├── sql/
│   ├── global_trends.sql
│   ├── country_analysis.sql
│   └── daily_stats.sql
├── functions/
│   ├── data_processor.py
│   └── dashboard_updater.py
└── dashboard/
    └── covid19_dashboard.json
```

## Analysis Features

1. Global COVID-19 Trends
   - Daily new cases
   - Cumulative cases
   - Death rates
   - Recovery rates

2. Country-wise Analysis
   - Top affected countries
   - Case fatality rates
   - Testing rates
   - Vaccination progress

3. Time-based Analysis
   - Weekly trends
   - Monthly comparisons
   - Seasonal patterns

## Dashboard Access

The dashboard is hosted on Google Data Studio and can be accessed at: [Dashboard Link] (to be added after deployment)

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 