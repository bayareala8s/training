-- Lab 5.3: Analyst-facing views with mandatory partition guardrails

CREATE OR REPLACE VIEW cnde_dev_datalake.v_orders_enriched AS
SELECT
  f.order_id,
  f.order_timestamp,
  f.order_status,
  f.order_amount_usd,
  f.year,
  f.month,
  f.day,
  c.customer_name,
  c.customer_segment,
  p.product_name,
  p.category
FROM cnde_dev_datalake.fact_orders f
INNER JOIN cnde_dev_datalake.dim_customer c ON f.customer_key = c.customer_key
INNER JOIN cnde_dev_datalake.dim_product p ON f.product_key = p.product_key;

-- Dashboard view: current month only (reduces accidental full scans)
CREATE OR REPLACE VIEW cnde_dev_datalake.v_revenue_current_month AS
SELECT
  report_day,
  category,
  SUM(revenue_usd) AS revenue_usd,
  SUM(order_count) AS order_count
FROM cnde_dev_datalake.daily_revenue_summary
WHERE year = CAST(YEAR(CURRENT_DATE) AS VARCHAR)
  AND month = LPAD(CAST(MONTH(CURRENT_DATE) AS VARCHAR), 2, '0')
GROUP BY report_day, category;
