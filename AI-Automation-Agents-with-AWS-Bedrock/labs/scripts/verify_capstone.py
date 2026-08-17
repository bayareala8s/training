#!/usr/bin/env python3
"""Integration verification for Week 8 capstone endpoints."""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import boto3

LABS_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LABS_ROOT))

FAILURES: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"FAIL: {msg}")


def ok(msg: str) -> None:
    print(f"OK: {msg}")


def load_stack_env() -> None:
    env_file = LABS_ROOT / ".stack.env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("export "):
                key, _, val = line[7:].partition("=")
                os.environ.setdefault(key, val.strip('"'))


def http_post(url: str, body: dict) -> tuple[int, dict]:
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode()) if e.fp else {"error": str(e)}


def main() -> int:
    load_stack_env()
    api_base = os.environ.get("API_ENDPOINT", "").rstrip("/")
    region = os.environ.get("AWS_REGION", "us-east-1")
    incident_sm = os.environ.get("CAPSTONE_INCIDENT_SM_ARN", "")
    approval_sm = os.environ.get("CAPSTONE_APPROVAL_SM_ARN", "")

    if not api_base:
        print("ERROR: Run ./scripts/start.sh first")
        return 1

    cid = f"capstone-verify-{int(time.time())}"

    # Option A — Incident triage
    code, out = http_post(f"{api_base}/capstone/incident", {
        "text": "API 503 after deployment in production",
        "correlation_id": f"{cid}-incident",
    })
    if code == 200 and out.get("ticket_stub"):
        ok(f"Capstone incident triage severity={out.get('ticket_stub', {}).get('severity')}")
    else:
        fail(f"Capstone /incident: {code} {out}")

    # Option B — Document classification
    code, out = http_post(f"{api_base}/capstone/document", {
        "document_text": "INVOICE #123 Amount Due $500",
        "correlation_id": f"{cid}-doc",
    })
    if code == 200 and out.get("result", {}).get("doc_type"):
        ok(f"Capstone document doc_type={out['result']['doc_type']} queue={out['result'].get('queue')}")
    else:
        fail(f"Capstone /document: {code} {out}")

    # Option C — Approval request (high risk)
    code, out = http_post(f"{api_base}/capstone/approval/request", {
        "action_text": "Delete production database credentials",
        "correlation_id": f"{cid}-apr",
    })
    approval_id = out.get("approval_id")
    if code in (200, 202) and approval_id and out.get("status") == "pending_approval":
        ok(f"Capstone approval pending id={approval_id}")
    else:
        fail(f"Capstone /approval/request: {code} {out}")

    # Option C — Approval decide
    if approval_id:
        code, out = http_post(f"{api_base}/capstone/approval/decide", {
            "approval_id": approval_id,
            "decision": "approve",
            "correlation_id": f"{cid}-apr",
            "approver_id": "verify-script",
        })
        if code == 200 and out.get("decision") == "approve":
            ok("Capstone approval decide=approve")
        else:
            fail(f"Capstone /approval/decide: {code} {out}")

    # Option D — Enterprise agent
    code, out = http_post(f"{api_base}/capstone/agent", {
        "text": "Summarize: DB failover in prod",
        "session_id": f"{cid}-sess",
        "correlation_id": f"{cid}-agent",
    })
    if code == 200 and out.get("tool"):
        ok(f"Capstone agent tool={out['tool']} policy={out.get('policy_decision')}")
    else:
        fail(f"Capstone /agent: {code} {out}")

    # Option A — Step Functions (if ARN available)
    if incident_sm:
        sfn = boto3.client("stepfunctions", region_name=region)
        resp = sfn.start_execution(
            stateMachineArn=incident_sm,
            input=json.dumps({
                "text": "Production API latency spike",
                "correlation_id": f"{cid}-sfn",
            }),
        )
        arn = resp["executionArn"]
        status = "RUNNING"
        for _ in range(40):
            desc = sfn.describe_execution(executionArn=arn)
            status = desc["status"]
            if status != "RUNNING":
                break
            time.sleep(3)
        if status == "SUCCEEDED":
            ok(f"Capstone incident SFN SUCCEEDED ({arn[-12:]})")
        else:
            fail(f"Capstone incident SFN {status}")

    # Option C — Approval Step Functions (if ARN available)
    if approval_sm:
        sfn = boto3.client("stepfunctions", region_name=region)
        resp = sfn.start_execution(
            stateMachineArn=approval_sm,
            input=json.dumps({
                "action_text": "Rotate production API keys",
                "correlation_id": f"{cid}-apr-sfn",
                "requester_id": "verify-script",
            }),
        )
        arn = resp["executionArn"]
        status = "RUNNING"
        for _ in range(40):
            desc = sfn.describe_execution(executionArn=arn)
            status = desc["status"]
            if status != "RUNNING":
                break
            time.sleep(3)
        if status == "SUCCEEDED":
            ok(f"Capstone approval SFN SUCCEEDED ({arn[-12:]})")
        else:
            fail(f"Capstone approval SFN {status}")

    print()
    if FAILURES:
        print(f"=== {len(FAILURES)} capstone check(s) failed ===")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("=== All capstone checks passed ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
