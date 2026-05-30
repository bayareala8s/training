-- Lab 5.1: Create Glue Data Catalog database (if not exists from Module 3)
-- Run in Athena. Replace {database} with your catalog name, e.g. cnde_dev_datalake

CREATE DATABASE IF NOT EXISTS cnde_dev_datalake
COMMENT 'RetailCo data lake — curated analytics (Module 5)'
LOCATION 's3://YOUR_BUCKET/curated/';
