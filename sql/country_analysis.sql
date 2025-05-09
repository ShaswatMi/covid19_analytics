-- Country-wise COVID-19 Analysis
WITH country_stats AS (
  SELECT
    country_name,
    date,
    new_confirmed,
    new_deceased,
    new_recovered,
    cumulative_confirmed,
    cumulative_deceased,
    cumulative_recovered,
    population
  FROM `bigquery-public-data.covid19_open_data.covid19_open_data`
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    AND country_name IS NOT NULL
),
latest_stats AS (
  SELECT
    country_name,
    MAX(date) as latest_date,
    SUM(new_confirmed) as total_new_cases_30d,
    SUM(new_deceased) as total_new_deaths_30d,
    SUM(new_recovered) as total_new_recovered_30d,
    MAX(cumulative_confirmed) as total_cases,
    MAX(cumulative_deceased) as total_deaths,
    MAX(cumulative_recovered) as total_recovered,
    MAX(population) as population
  FROM country_stats
  GROUP BY country_name
)
SELECT
  country_name,
  latest_date,
  total_new_cases_30d,
  total_new_deaths_30d,
  total_new_recovered_30d,
  total_cases,
  total_deaths,
  total_recovered,
  population,
  ROUND(SAFE_DIVIDE(total_cases, population) * 100000, 2) as cases_per_100k,
  ROUND(SAFE_DIVIDE(total_deaths, population) * 100000, 2) as deaths_per_100k,
  ROUND(SAFE_DIVIDE(total_deaths, total_cases) * 100, 2) as case_fatality_rate,
  ROUND(SAFE_DIVIDE(total_recovered, total_cases) * 100, 2) as recovery_rate
FROM latest_stats
WHERE total_cases > 0
ORDER BY total_cases DESC
LIMIT 50; 