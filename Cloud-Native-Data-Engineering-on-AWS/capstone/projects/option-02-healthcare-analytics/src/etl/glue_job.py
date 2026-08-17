"""
AWS Glue ETL job – Healthcare Analytics Platform (cnde-cap-healthcare)

Reads synthetic patient, appointment, and lab raw files from S3, applies
quality filters aligned with Lab 4.1 rules, masks PHI in curated patients
(SSN → ***-**-XXXX, email → SHA-256), and builds department appointment
summaries.

Job parameters:
  --JOB_NAME
  --BUCKET
  --PROCESSING_DATE
  --PROJECT          cnde-cap-healthcare

Local path uses patients_curated.py / appointments_curated.py instead.
All sample PHI is synthetic / fake.
"""

from __future__ import annotations

import hashlib
import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql.types import StringType


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


def sha256_email(email: str) -> str:
    if email is None:
        return ""
    return hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()


def main() -> None:
    args = parse_args()
    sc = SparkContext()
    glue_ctx = GlueContext(sc)
    spark = glue_ctx.spark_session
    job = Job(glue_ctx)
    job.init(args["JOB_NAME"], args)

    bucket = args["BUCKET"]
    processing_date = args["PROCESSING_DATE"]
    project = args.get("PROJECT", "cnde-cap-healthcare")

    hash_udf = F.udf(sha256_email, StringType())

    # --- Patients: validate + mask PHI ---
    patients = spark.read.option("header", True).csv(
        zone_path(bucket, "raw", "patients", processing_date)
    )
    patients_typed = patients.withColumn("age", F.col("age").cast("double"))
    patients_clean = patients_typed.filter(
        (F.col("patient_id").rlike(r"^PAT-[0-9]{6}$"))
        & (F.col("last_name").isNotNull())
        & (F.col("last_name") != "")
        & (F.col("age").between(0, 120))
        & (F.col("sex").isin(["F", "M", "X", "U"]))
        & (F.col("ssn").rlike(r"^[0-9]{3}-[0-9]{2}-[0-9]{4}$"))
        & (F.col("email").rlike(r"^[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}$"))
    )
    patients_quarantine = patients_typed.join(
        patients_clean.select("patient_id"), on="patient_id", how="left_anti"
    )
    patients_clean.write.mode("overwrite").json(
        zone_path(bucket, "cleaned", "patients", processing_date)
    )
    patients_quarantine.write.mode("overwrite").json(
        zone_path(bucket, "quarantine", "patients", processing_date)
    )

    patients_curated = (
        patients_clean.withColumn(
            "ssn_masked",
            F.concat(F.lit("***-**-"), F.substring(F.regexp_replace("ssn", "-", ""), -4, 4)),
        )
        .withColumn("email_hash", hash_udf(F.col("email")))
        .drop("ssn", "email")
        .withColumn("processing_date", F.lit(processing_date))
        .withColumn("pii_policy", F.lit("ssn_masked_last4;email_sha256"))
        .withColumn("project", F.lit(project))
    )
    patients_curated.write.mode("overwrite").option("header", True).csv(
        zone_path(bucket, "curated", "patients", processing_date)
    )

    # --- Appointments: department summary ---
    appointments = spark.read.option("header", True).csv(
        zone_path(bucket, "raw", "appointments", processing_date)
    )
    depts = [
        "cardiology",
        "oncology",
        "pediatrics",
        "orthopedics",
        "primary_care",
        "radiology",
    ]
    apt_clean = (
        appointments.withColumn("duration_minutes", F.col("duration_minutes").cast("double"))
        .filter(
            (F.col("appointment_id").rlike(r"^APT-[0-9]{8}-[0-9]{4}$"))
            & (F.col("patient_id").isNotNull())
            & (F.col("patient_id") != "")
            & (F.col("duration_minutes").between(5, 240))
            & (F.col("department").isin(depts))
            & (F.col("status").isin(["scheduled", "completed", "cancelled", "no_show"]))
            & (F.col("appointment_date").rlike(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"))
        )
    )
    apt_clean.write.mode("overwrite").json(
        zone_path(bucket, "cleaned", "appointments", processing_date)
    )

    dept_summary = (
        apt_clean.groupBy("department")
        .agg(
            F.count("*").alias("appointment_count"),
            F.sum(F.when(F.col("status") == "completed", 1).otherwise(0)).alias(
                "completed_count"
            ),
            F.sum(F.when(F.col("status") == "cancelled", 1).otherwise(0)).alias(
                "cancelled_count"
            ),
            F.sum(F.when(F.col("status") == "no_show", 1).otherwise(0)).alias(
                "no_show_count"
            ),
            F.sum("duration_minutes").alias("total_duration_minutes"),
            F.round(F.avg("duration_minutes"), 1).alias("avg_duration_minutes"),
        )
        .withColumn(
            "completion_rate_pct",
            F.round(F.col("completed_count") / F.col("appointment_count") * 100, 2),
        )
        .withColumn("processing_date", F.lit(processing_date))
        .withColumn("report_name", F.lit("appointments_by_department"))
    )
    dept_summary.write.mode("overwrite").option("header", True).csv(
        zone_path(bucket, "curated", "appointments", processing_date)
    )

    # --- Lab results ---
    labs = spark.read.json(zone_path(bucket, "raw", "lab_results", processing_date))
    lab_clean = (
        labs.withColumn("numeric_value", F.col("numeric_value").cast("double"))
        .filter(
            (F.col("result_id").rlike(r"^LAB-[0-9]{8}-[0-9]{4}$"))
            & (F.col("patient_id").isNotNull())
            & (F.col("patient_id") != "")
            & (F.col("numeric_value").between(0, 10000))
            & (F.col("test_code").isin(["CBC", "BMP", "LIPID", "A1C", "TSH", "COVID_PCR"]))
            & (F.col("result_flag").isin(["normal", "high", "low", "critical"]))
            & (F.col("collected_date").rlike(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"))
        )
        .withColumn("processing_date", F.lit(processing_date))
        .withColumn(
            "is_abnormal",
            F.col("result_flag").isin(["high", "low", "critical"]),
        )
    )
    lab_clean.write.mode("overwrite").option("header", True).csv(
        zone_path(bucket, "curated", "lab_results", processing_date)
    )

    job.commit()


if __name__ == "__main__":
    main()
