"""API entry Lambda — starts Step Functions execution and returns decision output."""
from __future__ import annotations

import json
import os
import time
import uuid

import boto3

SFN_ARN = os.environ["STATE_MACHINE_ARN"]
LAB_API_TOKEN = os.environ.get("LAB_API_TOKEN", "")
sfn = boto3.client("stepfunctions")


def handler(event, context):
    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    token = headers.get("x-lab-token", "")
    if LAB_API_TOKEN and token != LAB_API_TOKEN:
        return {
            "statusCode": 401,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"error": "unauthorized", "hint": "Pass header x-lab-token from terraform output api_token"}),
        }

    try:
        body = event.get("body") or "{}"
        if event.get("isBase64Encoded"):
            import base64

            body = base64.b64decode(body).decode("utf-8")
        payload = json.loads(body) if isinstance(body, str) else body
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"error": "invalid_json"}),
        }

    incident_id = payload.get("incident_id") or f"INC-{uuid.uuid4().hex[:8]}"
    incident_text = payload.get("incident_text")
    if not incident_text:
        return {
            "statusCode": 400,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"error": "incident_text_required"}),
        }

    execution = sfn.start_execution(
        stateMachineArn=SFN_ARN,
        name=f"{incident_id}-{uuid.uuid4().hex[:6]}"[:80],
        input=json.dumps({"incident_id": incident_id, "incident_text": incident_text}),
    )

    result = None
    for _ in range(30):
        d = sfn.describe_execution(executionArn=execution["executionArn"])
        if d["status"] != "RUNNING":
            result = d
            break
        time.sleep(0.5)

    if not result:
        return {
            "statusCode": 202,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(
                {
                    "incident_id": incident_id,
                    "status": "running",
                    "execution_arn": execution["executionArn"],
                }
            ),
        }

    if result["status"] != "SUCCEEDED":
        return {
            "statusCode": 500,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(
                {
                    "incident_id": incident_id,
                    "status": result["status"],
                    "execution_arn": execution["executionArn"],
                    "error": result.get("error"),
                    "cause": result.get("cause"),
                }
            ),
        }

    output = json.loads(result.get("output") or "{}")
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(output),
    }
