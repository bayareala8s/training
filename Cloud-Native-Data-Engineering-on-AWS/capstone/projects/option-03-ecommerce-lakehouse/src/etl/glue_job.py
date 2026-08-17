"""
AWS Glue ETL Job: E-Commerce Analytics Lakehouse (Option 3)

Course: Cloud-Native Data Engineering on AWS · Capstone Option 3
Project: cnde-cap-ecommerce

Reads validated order lines from the cleaned zone, builds fact_orders,
and writes Snappy Parquet to curated with Hive-style partitions.

Job parameters:
  JOB_NAME          - Glue job name
  raw_bucket        - S3 data lake bucket
  cleaned_bucket    - cleaned zone bucket (often same)
  curated_bucket    - curated zone bucket (often same)
  processing_date   - ISO date YYYY-MM-DD
"""

from __future__ import annotations

import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F


def parse_args() -> dict:
    return getResolvedOptions(
        sys.argv,
        [
            "JOB_NAME",
            "raw_bucket",
            "cleaned_bucket",
            "curated_bucket",
            "processing_date",
        ],
    )


def main() -> None:
    args = parse_args()
    sc = SparkContext()
    glue_ctx = GlueContext(sc)
    spark = glue_ctx.spark_session
    job = Job(glue_ctx)
    job.init(args["JOB_NAME"], args)

    year, month, day = args["processing_date"].split("-")
    cleaned = args["cleaned_bucket"]
    curated = args["curated_bucket"]

    orders_path = (
        f"s3://{cleaned}/cleaned/orders/year={year}/month={month}/day={day}/"
    )
    products_path = (
        f"s3://{cleaned}/cleaned/products/year={year}/month={month}/day={day}/"
    )

    orders = spark.read.json(orders_path)
    products = spark.read.json(products_path)

    fact_orders = (
        orders.withColumn("amount", F.col("order_amount").cast("double"))
        .withColumn("quantity", F.col("quantity").cast("int"))
        .withColumn("order_date", F.coalesce(F.col("order_date"), F.lit(args["processing_date"])))
        .withColumn("processing_date", F.lit(args["processing_date"]))
        .withColumn("gross_margin_proxy", F.round(F.col("amount") * F.lit(0.32), 2))
        .select(
            "order_id",
            "customer_id",
            "product_id",
            "amount",
            "quantity",
            "status",
            "channel",
            "order_date",
            "processing_date",
            "gross_margin_proxy",
        )
    )

    # Enrich with product category when available (star schema join)
    if "category" in products.columns:
        fact_orders = (
            fact_orders.join(
                products.select("product_id", "category", "unit_price"),
                on="product_id",
                how="left",
            )
        )

    out = (
        f"s3://{curated}/curated/fact_orders/"
        f"year={year}/month={month}/day={day}/"
    )
    (
        fact_orders.write.mode("overwrite")
        .option("compression", "snappy")
        .parquet(out)
    )

    job.commit()


if __name__ == "__main__":
    main()
