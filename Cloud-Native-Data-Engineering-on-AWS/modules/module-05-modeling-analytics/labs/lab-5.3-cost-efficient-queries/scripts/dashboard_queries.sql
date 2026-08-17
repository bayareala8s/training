-- Lab 5.3: Compare scan — fact table vs summary table

-- EXPENSIVE: ad hoc aggregation on fact (use only for backfills)
SELECT
  f.day,
  p.category,
  SUM(f.order_amount_usd) AS revenue_usd
FROM cnde_dev_datalake.fact_orders f
INNER JOIN cnde_dev_datalake.dim_product p ON f.product_key = p.product_key
WHERE f.year = '2024' AND f.month = '01' AND f.day BETWEEN '01' AND '07'
  AND f.order_status <> 'cancelled'
GROUP BY f.day, p.category;

-- EFFICIENT: query pre-aggregated summary
SELECT
  report_day,
  category,
  SUM(revenue_usd) AS revenue_usd
FROM cnde_dev_datalake.daily_revenue_summary
WHERE year = '2024' AND month = '01'
  AND report_day BETWEEN '01' AND '07'
GROUP BY report_day, category
ORDER BY report_day, category;

-- EFFICIENT: analyst view with explicit partition
SELECT category, SUM(revenue_usd) AS revenue
FROM cnde_dev_datalake.v_revenue_current_month
GROUP BY category;
