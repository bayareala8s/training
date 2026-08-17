"""
AWS Glue ETL job – Banking Regulatory Data Platform (cnde-cap-banking)

Reads partitioned raw settlement and transaction files from S3, applies
declarative quality gates (mirrored from Lab 4.1 rules), writes cleaned /
quarantine zones, and materializes curated daily_settlement_summary.

Job parameters (Glue console / --arguments):
  --JOB_NAME
  --BUCKET           e.g. student-datalake-bucket
  --PROCESSING_DATE  e.g. 2024-01-15
  --PROJECT          cnde-cap-banking

Local note: this script is Glue/PySpark-oriented. The course local runner
uses the pandas-free curated modules (settlements_curated.py, etc.).
"""

from __future__ import annotations

import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F


def parse_args():
    return getResolvedOptions(
        sys.argv,
        ["JOB_NAME", "BUCKET", "PROCESSING_DATE", "PROJECT"],
    )


def zone_path(bucket: str, zone: str, dataset: str, processing_date: str) -> str:
    year, month, day = processing_date.split("-")
    return (
        f"s3://{bucket}/{zone}/{dataset}/"
        f"year={year}/month={month}/day={day}/"
    )


def main() -> None:
    args = parse_args()
    sc = SparkContext()
    glue_ctx = GlueContext(sc)
    spark = glue_ctx.spark_session
    job = Job(glue_ctx)
    job.init(args["JOB_NAME"], args)

    bucket = args["BUCKET"]
    processing_date = args["PROCESSING_DATE"]
    project = args.get("PROJECT", "cnde-cap-banking")

    # --- Settlements: raw → quality filter → curated daily_settlement_summary ---
    settlements = spark.read.option("header", True).csv(
        zone_path(bucket, "raw", "settlements", processing_date)
    )

    valid_currencies = ["USD", "EUR", "GBP", "CAD"]
    valid_statuses = ["completed", "pending", "failed", "reconciled"]

    settlements_typed = (
        settlements.withColumn("gross_amount", F.col("gross_amount").cast("double"))
        .withColumn("net_amount", F.col("net_amount").cast("double"))
        .withColumn("fee_amount", F.col("fee_amount").cast("double"))
    )

    settlements_clean = settlements_typed.filter(
        (F.col("settlement_id").rlike(r"^STL-[0-9]{8}-[A-Z0-9]{4}$"))
        & (F.col("settlement_date").isNotNull())
        & (F.col("settlement_date") != "")
        & (F.col("gross_amount").between(0.01, 50000000))
        & (F.col("net_amount").between(0.01, 50000000))
        & (F.col("currency").isin(valid_currencies))
        & (F.col("status").isin(valid_statuses))
    )

    settlements_quarantine = settlements_typed.join(
        settlements_clean.select("settlement_id"),
        on="settlement_id",
        how="left_anti",
    )

    settlements_clean.write.mode("overwrite").json(
        zone_path(bucket, "cleaned", "settlements", processing_date)
    )
    settlements_quarantine.write.mode("overwrite").json(
        zone_path(bucket, "quarantine", "settlements", processing_date)
    )

    daily_summary = (
        settlements_clean.groupBy("settlement_date", "currency", "status")
        .agg(
            F.count("*").alias("settlement_count"),
            F.round(F.sum("gross_amount"), 2).alias("gross_amount_sum"),
            F.round(F.sum("net_amount"), 2).alias("net_amount_sum"),
            F.round(F.sum("fee_amount"), 2).alias("fee_amount_sum"),
            F.round(F.avg("net_amount"), 2).alias("avg_net_amount"),
        )
        .withColumn("processing_date", F.lit(processing_date))
        .withColumn("report_name", F.lit("daily_settlement_summary"))
        .withColumn("project", F.lit(project))
    )

    daily_summary.write.mode("overwrite").option("header", True).csv(
        zone_path(bucket, "curated", "settlements", processing_date)
    )

    # --- Transactions: enrich for audit trail ---
    transactions = spark.read.option("header", True).csv(
        zone_path(bucket, "raw", "transactions", processing_date)
    )
    txn_clean = (
        transactions.withColumn("amount", F.col("amount").cast("double"))
        .filter(
            (F.col("transaction_id").rlike(r"^TXN-[0-9]{8}-[0-9]{4}$"))
            & (F.col("account_id").isNotNull())
            & (F.col("account_id") != "")
            & (F.col("amount").between(0.01, 1000000))
            & (F.col("currency").isin(valid_currencies))
            & (F.col("status").isin(["posted", "pending", "reversed", "settled"]))
            & (F.col("settlement_date").rlike(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"))
        )
        .withColumn("processing_date", F.lit(processing_date))
        .withColumn("is_high_value", F.col("amount") >= F.lit(10000))
    )
    txn_clean.write.mode("overwrite").option("header", True).csv(
        zone_path(bucket, "curated", "transactions", processing_date)
    )

    # --- Accounts master ---
    accounts = spark.read.json(zone_path(bucket, "raw", "accounts", processing_date))
    accounts_clean = (
        accounts.withColumn("balance", F.col("balance").cast("double"))
        .filter(
            (F.col("account_id").rlike(r"^ACC-[0-9]{6}$"))
            & (F.col("customer_name").isNotNull())
            & (F.col("customer_name") != "")
            & (F.col("balance").between(-50000, 10000000))
            & (
                F.col("account_type").isin(
                    ["checking", "savings", "money_market", "brokerage"]
                )
            )
            & (F.col("status").isin(["active", "dormant", "closed", "frozen"]))
        )
        .withColumn("processing_date", F.lit(processing_date))
        .withColumn("is_overdrawn", F.col("balance") < 0)
    )
    accounts_clean.write.mode("overwrite").option("header", True).csv(
        zone_path(bucket, "curated", "accounts", processing_date)
    )

    job.commit()


if __name__ == "__main__":
    main()
