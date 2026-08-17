#!/usr/bin/env python3
"""
Integration verification for deployed AWS labs.
Exits 0 only if all checks pass. Requires stack from ./scripts/start.sh
"""

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


def http_post(url: str, body: dict, headers: dict | None = None, *, expect_error: bool = False) -> dict:
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode() if e.fp else ""
        if expect_error:
            try:
                return json.loads(err_body)
            except json.JSONDecodeError:
                return {"error": err_body, "status_code": e.code}
        fail(f"HTTP {e.code} for {url}: {err_body[:500]}")
        raise


def check_week2_lambda(region: str, function_name: str, cid: str) -> None:
    client = boto3.client("lambda", region_name=region)
    payload = json.dumps({"prompt": "Reply with one word: ok", "correlation_id": cid})
    resp = client.invoke(
        FunctionName=function_name,
        Payload=payload.encode(),
    )
    body = json.loads(resp["Payload"].read())
    if not body.get("success"):
        fail(f"Week2 Lambda: {body}")
    else:
        ok(f"Week2 Lambda invoke (latency_ms={body.get('latency_ms')})")


def check_api_classify(api_base: str, cid: str) -> None:
    url = f"{api_base.rstrip('/')}/classify"
    out = http_post(url, {"text": "I was charged twice on my invoice for March."}, {"X-Correlation-Id": cid})
    if not out.get("result") and not out.get("valid"):
        fail(f"API /classify: {out}")
    else:
        ok(f"API /classify label={out.get('result', {}).get('label')}")


def check_api_route_rules(api_base: str) -> None:
    url = f"{api_base.rstrip('/')}/route"
    out = http_post(
        url,
        {"text": "I was charged twice on my invoice", "label": "billing"},
    )
    source = out.get("source") or out.get("result", {}).get("source")
    route = out.get("result", {}).get("route") if isinstance(out.get("result"), dict) else out.get("route")
    if source == "rules" or route == "team_billing":
        ok(f"API /route rules path route={route} source={source}")
    else:
        fail(f"API /route expected rules/billing route: {out}")


def check_api_summarize(api_base: str, cid: str) -> None:
    url = f"{api_base.rstrip('/')}/summarize"
    out = http_post(
        url,
        {"text": "Database failover completed in us-east-1. No customer impact reported."},
        {"X-Correlation-Id": f"{cid}-sum"},
    )
    if not out.get("summary"):
        fail(f"API /summarize: {out}")
    else:
        ok(f"API /summarize returned summary ({len(out['summary'])} chars)")


def check_api_empty_input(api_base: str) -> None:
    url = f"{api_base.rstrip('/')}/classify"
    out = http_post(url, {"text": "   "}, expect_error=True)
    if out.get("error") == "text_required":
        ok("API /classify rejects empty input (400)")
    else:
        fail(f"API /classify expected text_required, got: {out}")


def check_api_input_limit(api_base: str) -> None:
    url = f"{api_base.rstrip('/')}/classify"
    big = "x" * 9000
    out = http_post(url, {"text": big}, expect_error=True)
    if out.get("error") == "input_too_large":
        ok("API /classify rejects oversized input (400)")
    else:
        fail(f"API /classify expected input_too_large, got: {out}")


def check_step_functions(region: str, sm_arn: str, cid: str) -> None:
    sfn = boto3.client("stepfunctions", region_name=region)
    ticket = "API 503 after deployment in production"
    resp = sfn.start_execution(
        stateMachineArn=sm_arn,
        input=json.dumps({"text": ticket, "correlation_id": cid}),
    )
    arn = resp["executionArn"]
    for _ in range(40):
        desc = sfn.describe_execution(executionArn=arn)
        status = desc["status"]
        if status != "RUNNING":
            break
        time.sleep(3)
    if status != "SUCCEEDED":
        err = desc.get("error") or ""
        cause = desc.get("cause") or ""
        fail(f"Step Functions execution {status}: {err} {cause[:400]}")
    else:
        ok(f"Step Functions workflow SUCCEEDED ({arn[-12:]})")


def check_agent(region: str, function_name: str, cid: str) -> None:
    client = boto3.client("lambda", region_name=region)
    payload = json.dumps(
        {
            "text": "Summarize: database failover completed",
            "session_id": f"{cid}-sess",
            "correlation_id": cid,
        }
    )
    resp = client.invoke(FunctionName=function_name, Payload=payload.encode())
    body = json.loads(resp["Payload"].read())
    if not body.get("plan") or not body.get("tool"):
        fail(f"Agent Lambda: {body}")
    else:
        ok(f"Agent Lambda tool={body.get('tool')} policy={body.get('policy_decision')}")


def check_audit_table(region: str, table_name: str, cid: str) -> None:
    os.environ["AUDIT_TABLE_NAME"] = table_name
    os.environ["AWS_REGION"] = region
    from common.audit import query_by_correlation

    items = []
    for _ in range(8):
        items = query_by_correlation(f"{cid}-api")
        if items:
            break
        time.sleep(2)
    if items:
        ok(f"Audit table has {len(items)} event(s) for correlation {cid}-api")
    else:
        fail(f"No audit rows for {cid}-api (table={table_name})")


def main() -> int:
    load_stack_env()
    region = os.environ.get("AWS_REGION", "us-east-1")
    prefix = os.environ.get("PROJECT_PREFIX", "ba-la8s-ai")
    api_base = os.environ.get("API_ENDPOINT", "")
    sm_arn = os.environ.get("STATE_MACHINE_ARN", "")
    audit_table = os.environ.get("AUDIT_TABLE_NAME", f"{prefix}-audit")
    week2_fn = os.environ.get("WEEK2_FUNCTION", f"{prefix}-week2-invoke")
    agent_fn = os.environ.get("AGENT_FUNCTION", f"{prefix}-agent")

    if not api_base or not sm_arn:
        print("ERROR: Stack not configured. Run ./scripts/start.sh first.")
        return 1

    cid = f"verify-{int(time.time())}"
    print(f"Correlation prefix: {cid}\n")

    check_week2_lambda(region, week2_fn, f"{cid}-w2")
    check_api_classify(api_base, f"{cid}-api")
    check_api_summarize(api_base, cid)
    check_api_route_rules(api_base)
    check_api_empty_input(api_base)
    check_api_input_limit(api_base)
    check_step_functions(region, sm_arn, f"{cid}-sfn")
    check_agent(region, agent_fn, f"{cid}-agent")
    check_audit_table(region, audit_table, cid)

    print()
    if FAILURES:
        print(f"=== {len(FAILURES)} check(s) failed ===")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("=== All integration checks passed ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
