-- Global COVID-19 Trends Analysis
WITH daily_stats AS (
  SELECT
    date,
    SUM(new_confirmed) as global_new_cases,
    SUM(new_deceased) as global_new_deaths,
    SUM(new_recovered) as global_new_recovered,
    SUM(cumulative_confirmed) as global_total_cases,
    SUM(cumulative_deceased) as global_total_deaths,
    SUM(cumulative_recovered) as global_total_recovered
  FROM `bigquery-public-data.covid19_open_data.covid19_open_data`
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
  GROUP BY date
  ORDER BY date
),
rolling_averages AS (
  SELECT
    date,
    global_new_cases,
    global_new_deaths,
    global_new_recovered,
    global_total_cases,
    global_total_deaths,
    global_total_recovered,
    AVG(global_new_cases) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as cases_7d_avg,
    AVG(global_new_deaths) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as deaths_7d_avg,
    AVG(global_new_recovered) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as recovered_7d_avg
  FROM daily_stats
)
SELECT
  date,
  global_new_cases,
  global_new_deaths,
  global_new_recovered,
  global_total_cases,
  global_total_deaths,
  global_total_recovered,
  cases_7d_avg,
  deaths_7d_avg,
  recovered_7d_avg,
  ROUND(SAFE_DIVIDE(global_new_deaths, global_new_cases) * 100, 2) as case_fatality_rate,
  ROUND(SAFE_DIVIDE(global_new_recovered, global_new_cases) * 100, 2) as recovery_rate
FROM rolling_averages
ORDER BY date DESC; 