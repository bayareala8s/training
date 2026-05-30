-- Lab 5.1: Load fact_orders from cleaned + dimension surrogate keys
-- Run per processing day or date range. Partition columns must match S3 paths.

INSERT INTO cnde_dev_datalake.fact_orders
SELECT
  ROW_NUMBER() OVER (ORDER BY o.order_id) AS order_key,
  o.order_id,
  dc.customer_key,
  dp.product_key,
  CAST(o.order_timestamp AS TIMESTAMP) AS order_timestamp,
  o.status AS order_status,
  COALESCE(o.quantity, 1) AS quantity,
  COALESCE(o.unit_price, o.order_amount) AS unit_price_usd,
  COALESCE(o.discount_amount, 0.0) AS discount_amount_usd,
  o.order_amount AS order_amount_usd,
  COALESCE(o.currency, 'USD') AS currency,
  o.fulfillment_hours,
  COALESCE(o.source_system, 'glue-etl') AS source_system,
  COALESCE(o.etl_batch_id, 'manual-lab-5.1') AS etl_batch_id,
  o.year,
  o.month,
  o.day
FROM cnde_dev_datalake.cleaned_retail_orders o
INNER JOIN cnde_dev_datalake.dim_customer dc
  ON o.customer_id = dc.customer_id
INNER JOIN cnde_dev_datalake.dim_product dp
  ON o.sku = dp.sku
WHERE o.year = '2024'
  AND o.month = '01'
  AND o.day = '15'
  AND o.status IN ('pending', 'shipped', 'delivered', 'cancelled')
  AND o.order_amount > 0;

-- Repair partitions after insert
-- MSCK REPAIR TABLE cnde_dev_datalake.fact_orders;
