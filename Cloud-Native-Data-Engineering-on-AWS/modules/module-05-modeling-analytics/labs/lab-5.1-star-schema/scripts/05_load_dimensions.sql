-- Lab 5.1: Populate dimensions from cleaned orders (CTAS pattern)
-- Prerequisites: cleaned_retail_orders table exists (Module 3 crawler)
-- Replace YOUR_BUCKET before running

-- ---------------------------------------------------------------------------
-- dim_customer: derive distinct customers from cleaned orders
-- ---------------------------------------------------------------------------
CREATE TABLE cnde_dev_datalake.dim_customer_staging
WITH (
  format = 'PARQUET',
  external_location = 's3://YOUR_BUCKET/curated/retail/dim_customer/',
  parquet_compression = 'SNAPPY'
) AS
SELECT
  ROW_NUMBER() OVER (ORDER BY customer_id) AS customer_key,
  customer_id,
  MAX(customer_name) AS customer_name,
  MAX(customer_email) AS email,
  COALESCE(MAX(customer_segment), 'standard') AS customer_segment,
  COALESCE(MAX(acquisition_channel), 'organic') AS acquisition_channel,
  COALESCE(MAX(country_code), 'US') AS country_code,
  CAST(MIN(order_date) AS DATE) AS first_order_date,
  TRUE AS is_active,
  CURRENT_TIMESTAMP AS updated_at
FROM cnde_dev_datalake.cleaned_retail_orders
WHERE customer_id IS NOT NULL
GROUP BY customer_id;

-- After validation, drop staging name or rename via crawler:
-- DROP TABLE IF EXISTS cnde_dev_datalake.dim_customer_staging;

-- ---------------------------------------------------------------------------
-- dim_product: derive from distinct SKUs in cleaned orders
-- ---------------------------------------------------------------------------
CREATE TABLE cnde_dev_datalake.dim_product_staging
WITH (
  format = 'PARQUET',
  external_location = 's3://YOUR_BUCKET/curated/retail/dim_product/',
  parquet_compression = 'SNAPPY'
) AS
SELECT
  ROW_NUMBER() OVER (ORDER BY sku) AS product_key,
  sku,
  MAX(product_name) AS product_name,
  COALESCE(MAX(category), 'uncategorized') AS category,
  COALESCE(MAX(subcategory), 'general') AS subcategory,
  COALESCE(MAX(brand), 'unknown') AS brand,
  AVG(COALESCE(unit_cost, 0.0)) AS unit_cost_usd,
  AVG(COALESCE(unit_price, order_amount)) AS unit_price_usd,
  TRUE AS is_active,
  CURRENT_TIMESTAMP AS updated_at
FROM cnde_dev_datalake.cleaned_retail_orders
WHERE sku IS NOT NULL
GROUP BY sku;
