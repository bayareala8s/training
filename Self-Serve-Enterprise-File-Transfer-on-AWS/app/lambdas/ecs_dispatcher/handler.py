"""Dispatch ECS Fargate worker when large files land in S3."""
import json
import os
from urllib.parse import unquote_plus

import boto3

ecs = boto3.client("ecs")

CLUSTER = os.environ["ECS_CLUSTER"]
TASK_DEFINITION = os.environ["TASK_DEFINITION"]
SUBNETS = os.environ["SUBNETS"].split(",")
SECURITY_GROUPS = os.environ["SECURITY_GROUPS"].split(",")
DEST_PREFIX = os.environ.get("DEST_PREFIX", "partners/demo/large/processed/")


def handler(event, context):
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])
        if key.endswith("/") or key.endswith(".manifest.json"):
            continue

        correlation_id = record.get("responseElements", {}).get("x-amz-request-id", key)
        job = {
            "bucket": bucket,
            "source_key": key,
            "dest_prefix": DEST_PREFIX,
            "correlation_id": correlation_id,
        }

        resp = ecs.run_task(
            cluster=CLUSTER,
            taskDefinition=TASK_DEFINITION,
            launchType="FARGATE",
            networkConfiguration={
                "awsvpcConfiguration": {
                    "subnets": SUBNETS,
                    "securityGroups": SECURITY_GROUPS,
                    "assignPublicIp": "ENABLED",
                }
            },
            overrides={
                "containerOverrides": [
                    {
                        "name": "worker",
                        "environment": [
                            {"name": "TRANSFER_JOB", "value": json.dumps(job)},
                        ],
                    }
                ]
            },
        )
        failures = resp.get("failures", [])
        if failures:
            raise RuntimeError(f"ECS RunTask failed: {failures}")

        task_arn = resp["tasks"][0]["taskArn"]
        print(json.dumps({"dispatched": task_arn, "job": job}))

    return {"statusCode": 200}
