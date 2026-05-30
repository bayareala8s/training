-- Lab 5.2: AFTER optimization — compare Data scanned to before_queries.sql

-- Query A1: Partition pruning — single day
SELECT
  SUM(order_amount_usd) AS revenue_usd,
  COUNT(*) AS order_count
FROM cnde_dev_datalake.fact_orders
WHERE year = '2024'
  AND month = '01'
  AND day = '15'
  AND order_status <> 'cancelled';

-- Query A2: Column projection — only needed fields
SELECT
  customer_key,
  order_amount_usd,
  order_status
FROM cnde_dev_datalake.fact_orders
WHERE year = '2024'
  AND month = '01'
  AND day BETWEEN '01' AND '07'
  AND order_status = 'shipped';

-- Query A3: Literal partition predicates (pruning-friendly)
SELECT SUM(order_amount_usd) AS revenue
FROM cnde_dev_datalake.fact_orders
WHERE year = '2024'
  AND month = '01'
  AND day IN ('01', '02', '03', '04', '05', '06', '07');

-- Query A4: Filter fact before join
SELECT
  c.customer_name,
  p.category,
  SUM(f.order_amount_usd) AS revenue
FROM (
  SELECT customer_key, product_key, order_amount_usd
  FROM cnde_dev_datalake.fact_orders
  WHERE year = '2024'
    AND month = '01'
    AND day = '15'
    AND order_status = 'shipped'
) f
INNER JOIN cnde_dev_datalake.dim_customer c ON f.customer_key = c.customer_key
INNER JOIN cnde_dev_datalake.dim_product p ON f.product_key = p.product_key
GROUP BY c.customer_name, p.category
ORDER BY revenue DESC
LIMIT 20;
