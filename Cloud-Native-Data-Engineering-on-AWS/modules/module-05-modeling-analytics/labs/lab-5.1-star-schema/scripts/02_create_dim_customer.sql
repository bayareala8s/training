-- Lab 5.1: dim_customer — SCD Type 1 (current state only)
-- S3 layout: s3://{bucket}/curated/retail/dim_customer/

CREATE EXTERNAL TABLE IF NOT EXISTS cnde_dev_datalake.dim_customer (
  customer_key        BIGINT,
  customer_id         STRING,
  customer_name       STRING,
  email               STRING,
  customer_segment    STRING,
  acquisition_channel STRING,
  country_code        STRING,
  first_order_date    DATE,
  is_active           BOOLEAN,
  updated_at          TIMESTAMP
)
STORED AS PARQUET
LOCATION 's3://YOUR_BUCKET/curated/retail/dim_customer/'
TBLPROPERTIES (
  'parquet.compression' = 'SNAPPY',
  'classification' = 'dimension',
  'domain' = 'retail'
);
