-- Lab 5.3: Pre-aggregated summary table for dashboard queries

CREATE TABLE IF NOT EXISTS cnde_dev_datalake.daily_revenue_summary
WITH (
  format = 'PARQUET',
  partitioned_by = ARRAY['year', 'month'],
  external_location = 's3://YOUR_BUCKET/curated/retail/daily_revenue_summary/',
  parquet_compression = 'SNAPPY'
) AS
SELECT
  f.day AS report_day,
  p.category,
  f.order_status,
  COUNT(DISTINCT f.order_id) AS order_count,
  SUM(f.order_amount_usd) AS revenue_usd,
  SUM(f.discount_amount_usd) AS total_discount_usd,
  AVG(f.fulfillment_hours) AS avg_fulfillment_hours,
  f.year,
  f.month
FROM cnde_dev_datalake.fact_orders f
INNER JOIN cnde_dev_datalake.dim_product p ON f.product_key = p.product_key
WHERE f.year = '2024'
  AND f.month = '01'
  AND f.order_status <> 'cancelled'
GROUP BY f.year, f.month, f.day, p.category, f.order_status;
