"""
AWS Glue ETL Job: Raw CSV → Cleaned Parquet (Retail Orders)

Course: Cloud-Native Data Engineering on AWS · Module 3 · Lab 3.1

Reads order CSV from the raw zone, applies validation and typing,
writes Snappy Parquet to the cleaned zone with Hive-style partitions.

Job parameters (passed via Glue default_arguments or --arguments):
  JOB_NAME          - Glue job name (required by Glue runtime)
  raw_bucket        - S3 bucket containing raw/ prefix
  cleaned_bucket    - S3 bucket for cleaned/ output (often same bucket)
  dataset_path      - Dataset path under zone, e.g. retail/orders
  processing_date   - ISO date YYYY-MM-DD for partition and input file
"""

import sys
from typing import List

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

# ---------------------------------------------------------------------------
# Schema contract for cleaned retail orders (extends Module 1 raw CSV)
# ---------------------------------------------------------------------------
CLEANED_SCHEMA = StructType(
    [
        StructField("order_id", StringType(), False),
        StructField("customer_id", StringType(), True),
        StructField("product_category", StringType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("unit_price", DoubleType(), True),
        StructField("total_amount", DoubleType(), True),
        StructField("order_status", StringType(), True),
        StructField("order_timestamp", TimestampType(), True),
        StructField("region", StringType(), True),
        StructField("processed_at", TimestampType(), True),
        StructField("source_file", StringType(), True),
        StructField("year", StringType(), False),
        StructField("month", StringType(), False),
        StructField("day", StringType(), False),
    ]
)

VALID_STATUSES = ["pending", "shipped", "delivered", "cancelled"]


def parse_args() -> dict:
    """Resolve Glue job parameters from sys.argv."""
    return getResolvedOptions(
        sys.argv,
        [
            "JOB_NAME",
            "raw_bucket",
            "cleaned_bucket",
            "dataset_path",
            "processing_date",
        ],
    )


def build_paths(args: dict) -> tuple[str, str, str]:
    """Build S3 input path and cleaned output base from processing_date."""
    processing_date = args["processing_date"]
    year, month, day = processing_date.split("-")
    dataset = args["dataset_path"].strip("/")

    input_key = (
        f"raw/{dataset}/year={year}/month={month}/day={day}/"
        f"orders_{processing_date}.csv"
    )
    input_path = f"s3://{args['raw_bucket']}/{input_key}"
    output_base = f"s3://{args['cleaned_bucket']}/cleaned/{dataset}/"
    return input_path, output_base, f"{year}/{month}/{day}"


def read_raw_csv(spark, input_path: str) -> DataFrame:
    """Read raw CSV with header; infer types then enforce in transform."""
    return (
        spark.read.option("header", True)
        .option("mode", "PERMISSIVE")
        .option("columnNameOfCorruptRecord", "_corrupt_record")
        .csv(input_path)
    )


def transform_orders(
    df: DataFrame,
    processing_date: str,
    source_file: str,
) -> DataFrame:
    """
    Clean and standardize order records.

    - Drop duplicates on order_id
    - Filter null order_id and invalid status
    - Cast numeric and timestamp fields
    - Recompute total_amount for consistency
    - Add lineage and partition columns
    """
    year, month, day = processing_date.split("-")

    cleaned = (
        df.dropDuplicates(["order_id"])
        .filter(F.col("order_id").isNotNull())
    )

    if "_corrupt_record" in df.columns:
        cleaned = cleaned.filter(F.col("_corrupt_record").isNull())

    cleaned = (
        cleaned
        .withColumn("quantity", F.col("quantity").cast(IntegerType()))
        .withColumn("unit_price", F.col("unit_price").cast(DoubleType()))
        .withColumn(
            "total_amount",
            F.round(F.col("quantity") * F.col("unit_price"), 2),
        )
        .withColumn(
            "order_timestamp",
            F.to_timestamp(F.col("order_timestamp")),
        )
        .filter(F.col("order_status").isin(VALID_STATUSES))
        .withColumn("processed_at", F.current_timestamp())
        .withColumn("source_file", F.lit(source_file))
        .withColumn("year", F.lit(year))
        .withColumn("month", F.lit(month))
        .withColumn("day", F.lit(day))
    )

    # Project to contract schema (ignores unexpected raw columns — schema evolution)
    column_order: List[str] = [f.name for f in CLEANED_SCHEMA.fields]
    return cleaned.select(*column_order)


def write_cleaned_parquet(df: DataFrame, output_base: str) -> None:
    """
    Write partitioned Parquet with dynamic partition overwrite.

    Only partitions present in the DataFrame are replaced on rerun.
    """
    spark = df.sparkSession
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

    (
        df.write.mode("overwrite")
        .option("compression", "snappy")
        .partitionBy("year", "month", "day")
        .parquet(output_base)
    )


def main() -> None:
    args = parse_args()
    input_path, output_base, partition_label = build_paths(args)

    sc = SparkContext()
    glue_context = GlueContext(sc)
    spark = glue_context.spark_session
    job = Job(glue_context)
    job.init(args["JOB_NAME"], args)

    print(f"[INFO] Reading raw CSV: {input_path}")
    raw_df = read_raw_csv(spark, input_path)
    raw_count = raw_df.count()
    print(f"[INFO] Raw record count: {raw_count}")

    if raw_count == 0:
        raise ValueError(
            f"No records found at {input_path}. "
            "Upload sample data from Module 1 Lab 1.2 first."
        )

    cleaned_df = transform_orders(
        raw_df,
        args["processing_date"],
        source_file=input_path,
    )
    clean_count = cleaned_df.count()
    quarantined = raw_count - clean_count
    print(f"[INFO] Cleaned record count: {clean_count}")
    print(f"[INFO] Records filtered (approx): {quarantined}")

    write_cleaned_parquet(cleaned_df, output_base)
    print(f"[INFO] Wrote Parquet to {output_base} partition {partition_label}")

    job.commit()


if __name__ == "__main__":
    main()
