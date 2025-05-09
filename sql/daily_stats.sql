-- Daily COVID-19 Statistics Analysis
WITH daily_metrics AS (
  SELECT
    date,
    country_name,
    new_confirmed,
    new_deceased,
    new_recovered,
    cumulative_confirmed,
    cumulative_deceased,
    cumulative_recovered,
    population
  FROM `bigquery-public-data.covid19_open_data.covid19_open_data`
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    AND country_name IS NOT NULL
),
daily_summary AS (
  SELECT
    date,
    COUNT(DISTINCT country_name) as countries_with_cases,
    SUM(new_confirmed) as total_new_cases,
    SUM(new_deceased) as total_new_deaths,
    SUM(new_recovered) as total_new_recovered,
    SUM(cumulative_confirmed) as total_cases,
    SUM(cumulative_deceased) as total_deaths,
    SUM(cumulative_recovered) as total_recovered,
    SUM(population) as total_population
  FROM daily_metrics
  GROUP BY date
),
top_countries AS (
  SELECT
    date,
    country_name,
    new_confirmed,
    new_deceased,
    new_recovered,
    ROUND(SAFE_DIVIDE(new_confirmed, population) * 100000, 2) as new_cases_per_100k,
    ROUND(SAFE_DIVIDE(new_deceased, population) * 100000, 2) as new_deaths_per_100k
  FROM daily_metrics
  WHERE new_confirmed > 0
  QUALIFY ROW_NUMBER() OVER (PARTITION BY date ORDER BY new_confirmed DESC) <= 10
)
SELECT
  d.date,
  d.countries_with_cases,
  d.total_new_cases,
  d.total_new_deaths,
  d.total_new_recovered,
  d.total_cases,
  d.total_deaths,
  d.total_recovered,
  ROUND(SAFE_DIVIDE(d.total_new_cases, d.total_population) * 100000, 2) as global_new_cases_per_100k,
  ROUND(SAFE_DIVIDE(d.total_new_deaths, d.total_population) * 100000, 2) as global_new_deaths_per_100k,
  ROUND(SAFE_DIVIDE(d.total_new_deaths, d.total_new_cases) * 100, 2) as global_case_fatality_rate,
  ROUND(SAFE_DIVIDE(d.total_new_recovered, d.total_new_cases) * 100, 2) as global_recovery_rate,
  ARRAY_AGG(STRUCT(
    t.country_name,
    t.new_confirmed,
    t.new_deceased,
    t.new_recovered,
    t.new_cases_per_100k,
    t.new_deaths_per_100k
  ) ORDER BY t.new_confirmed DESC) as top_10_countries
FROM daily_summary d
LEFT JOIN top_countries t ON d.date = t.date
GROUP BY
  d.date,
  d.countries_with_cases,
  d.total_new_cases,
  d.total_new_deaths,
  d.total_new_recovered,
  d.total_cases,
  d.total_deaths,
  d.total_recovered,
  d.total_population
ORDER BY d.date DESC; 