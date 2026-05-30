-- Lab 5.2: BEFORE optimization — intentionally inefficient patterns
-- Record "Data scanned" from Athena console for each query

-- Query B1: No partition filter (full table scan)
SELECT
  customer_key,
  order_id,
  order_amount_usd,
  order_status,
  order_timestamp,
  quantity,
  unit_price_usd,
  discount_amount_usd,
  currency,
  fulfillment_hours
FROM cnde_dev_datalake.fact_orders;

-- Query B2: SELECT * with wide date range
SELECT *
FROM cnde_dev_datalake.fact_orders
WHERE year = '2024';

-- Query B3: Function on partition column (blocks pruning)
SELECT SUM(order_amount_usd) AS revenue
FROM cnde_dev_datalake.fact_orders
WHERE CAST(concat(year, '-', month, '-', day) AS DATE)
  BETWEEN DATE '2024-01-01' AND DATE '2024-01-31';

-- Query B4: Join before filtering fact
SELECT
  c.customer_name,
  p.product_name,
  f.order_amount_usd
FROM cnde_dev_datalake.fact_orders f
INNER JOIN cnde_dev_datalake.dim_customer c ON f.customer_key = c.customer_key
INNER JOIN cnde_dev_datalake.dim_product p ON f.product_key = p.product_key
WHERE f.order_status = 'shipped';
