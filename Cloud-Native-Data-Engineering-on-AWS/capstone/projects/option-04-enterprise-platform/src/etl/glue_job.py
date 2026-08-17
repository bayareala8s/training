"""
AWS Glue ETL Job: Enterprise Data Platform (Option 4)

Course: Cloud-Native Data Engineering on AWS · Capstone Option 4
Project: cnde-cap-enterprise

Builds two curated products from cleaned zones:
  1) enterprise_kpi_daily – inventory + order volume KPIs
  2) customer_order_features – ML-ready customer aggregates

Job parameters:
  JOB_NAME          - Glue job name
  raw_bucket        - S3 data lake bucket
  cleaned_bucket    - cleaned zone bucket
  curated_bucket    - curated zone bucket
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
    partition = f"year={year}/month={month}/day={day}"

    orders = spark.read.json(f"s3://{cleaned}/cleaned/orders/{partition}/")
    inventory = spark.read.json(f"s3://{cleaned}/cleaned/inventory/{partition}/")

    orders_typed = (
        orders.withColumn("order_amount", F.col("order_amount").cast("double"))
        .withColumn("quantity", F.col("quantity").cast("int"))
    )

    inv_typed = inventory.withColumn(
        "quantity_on_hand", F.col("quantity_on_hand").cast("double")
    ).withColumn("reorder_point", F.col("reorder_point").cast("double"))

    order_kpis = orders_typed.agg(
        F.count("*").alias("order_count"),
        F.round(F.sum("order_amount"), 2).alias("gmv"),
        F.countDistinct("customer_id").alias("active_customers"),
    ).withColumn("kpi_date", F.lit(args["processing_date"]))

    inv_kpis = inv_typed.agg(
        F.countDistinct("sku").alias("sku_count"),
        F.countDistinct("warehouse_id").alias("warehouse_count"),
        F.sum("quantity_on_hand").cast("int").alias("total_units_on_hand"),
        F.sum(
            F.when(
                (F.col("stock_status") == "out_of_stock")
                | (F.col("quantity_on_hand") <= 0),
                1,
            ).otherwise(0)
        ).alias("stockout_skus"),
        F.round(F.avg("quantity_on_hand"), 2).alias("avg_quantity_on_hand"),
    ).withColumn("kpi_date", F.lit(args["processing_date"]))

    enterprise_kpi = order_kpis.join(inv_kpis, on="kpi_date", how="outer")
    kpi_out = f"s3://{curated}/curated/enterprise_kpi_daily/{partition}/"
    (
        enterprise_kpi.write.mode("overwrite")
        .option("compression", "snappy")
        .parquet(kpi_out)
    )

    features = (
        orders_typed.groupBy("customer_id")
        .agg(
            F.count("*").alias("order_count_30d"),
            F.round(F.sum("order_amount"), 2).alias("gmv_30d"),
            F.round(F.avg("order_amount"), 2).alias("avg_order_value"),
            F.sum("quantity").alias("units_ordered"),
            F.round(
                F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0))
                / F.count("*"),
                4,
            ).alias("cancel_rate"),
            F.countDistinct("business_unit").alias("business_unit_diversity"),
        )
        .withColumn("feature_date", F.lit(args["processing_date"]))
    )

    feat_out = f"s3://{curated}/curated/customer_order_features/{partition}/"
    (
        features.write.mode("overwrite")
        .option("compression", "snappy")
        .parquet(feat_out)
    )

    job.commit()


if __name__ == "__main__":
    main()
