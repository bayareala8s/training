"""
AWS Glue ETL Job (Optimized): Raw CSV → Cleaned Parquet

Module 3 · Lab 3.3 — extends Lab 3.1 with coalescing and Spark tuning.
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

# Target files per partition — increase for larger datasets
TARGET_FILES_PER_PARTITION = 1


def parse_args() -> dict:
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
    year, month, day = processing_date.split("-")
    cleaned = (
        df.dropDuplicates(["order_id"])
        .filter(F.col("order_id").isNotNull())
        .filter(F.col("_corrupt_record").isNull())
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
    column_order: List[str] = [f.name for f in CLEANED_SCHEMA.fields]
    return cleaned.select(*column_order)


def write_cleaned_parquet(
    df: DataFrame,
    output_base: str,
    target_files: int = TARGET_FILES_PER_PARTITION,
) -> None:
    spark = df.sparkSession
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    spark.conf.set("spark.sql.parquet.compression.codec", "snappy")
    spark.conf.set("spark.sql.adaptive.enabled", "true")
    spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

    df_out = df.coalesce(target_files)

    (
        df_out.write.mode("overwrite")
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
        raise ValueError(f"No records found at {input_path}")

    cleaned_df = transform_orders(
        raw_df,
        args["processing_date"],
        source_file=input_path,
    )
    clean_count = cleaned_df.count()
    print(f"[INFO] Cleaned record count: {clean_count}")
    print(f"[INFO] Target files per partition: {TARGET_FILES_PER_PARTITION}")

    write_cleaned_parquet(cleaned_df, output_base)
    print(f"[INFO] Wrote optimized Parquet to {output_base} partition {partition_label}")

    job.commit()


if __name__ == "__main__":
    main()
