-- Lab 5.1: fact_orders — grain: one row per order_id
-- Partitioned by year, month, day (aligned with cleaned zone from Module 3)

CREATE EXTERNAL TABLE IF NOT EXISTS cnde_dev_datalake.fact_orders (
  order_key           BIGINT,
  order_id            STRING,
  customer_key        BIGINT,
  product_key         BIGINT,
  order_timestamp     TIMESTAMP,
  order_status        STRING,
  quantity            INT,
  unit_price_usd      DOUBLE,
  discount_amount_usd DOUBLE,
  order_amount_usd    DOUBLE,
  currency            STRING,
  fulfillment_hours   DOUBLE,
  source_system       STRING,
  etl_batch_id        STRING
)
PARTITIONED BY (
  year  STRING,
  month STRING,
  day   STRING
)
STORED AS PARQUET
LOCATION 's3://YOUR_BUCKET/curated/retail/fact_orders/'
TBLPROPERTIES (
  'parquet.compression' = 'SNAPPY',
  'classification' = 'fact',
  'domain' = 'retail',
  'grain' = 'order_id'
);
