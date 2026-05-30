-- Lab 5.1: Star schema validation queries

-- Row counts
SELECT 'dim_customer' AS tbl, COUNT(*) AS cnt FROM cnde_dev_datalake.dim_customer
UNION ALL
SELECT 'dim_product', COUNT(*) FROM cnde_dev_datalake.dim_product
UNION ALL
SELECT 'fact_orders', COUNT(*) FROM cnde_dev_datalake.fact_orders
WHERE year = '2024' AND month = '01' AND day = '15';

-- Revenue by category (star join)
SELECT
  p.category,
  COUNT(DISTINCT f.order_id) AS order_count,
  SUM(f.order_amount_usd) AS revenue_usd
FROM cnde_dev_datalake.fact_orders f
INNER JOIN cnde_dev_datalake.dim_product p ON f.product_key = p.product_key
WHERE f.year = '2024' AND f.month = '01' AND f.day = '15'
  AND f.order_status <> 'cancelled'
GROUP BY p.category
ORDER BY revenue_usd DESC;

-- Referential integrity: orphaned facts should return 0 rows
SELECT f.order_id
FROM cnde_dev_datalake.fact_orders f
LEFT JOIN cnde_dev_datalake.dim_customer c ON f.customer_key = c.customer_key
WHERE f.year = '2024' AND f.month = '01' AND f.day = '15'
  AND c.customer_key IS NULL;
