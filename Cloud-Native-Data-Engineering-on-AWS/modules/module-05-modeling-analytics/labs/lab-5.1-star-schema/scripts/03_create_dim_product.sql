-- Lab 5.1: dim_product — product hierarchy flattened for star schema joins

CREATE EXTERNAL TABLE IF NOT EXISTS cnde_dev_datalake.dim_product (
  product_key     BIGINT,
  sku             STRING,
  product_name    STRING,
  category        STRING,
  subcategory     STRING,
  brand           STRING,
  unit_cost_usd   DOUBLE,
  unit_price_usd  DOUBLE,
  is_active       BOOLEAN,
  updated_at      TIMESTAMP
)
STORED AS PARQUET
LOCATION 's3://YOUR_BUCKET/curated/retail/dim_product/'
TBLPROPERTIES (
  'parquet.compression' = 'SNAPPY',
  'classification' = 'dimension',
  'domain' = 'retail'
);
