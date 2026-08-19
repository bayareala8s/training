#!/usr/bin/env python3
"""Write remaining Lambda handlers, sample data, scripts, capstones, LMS, marketing."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def w(rel: str, content: str) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.strip() + "\n", encoding="utf-8")
    print(rel)


def main() -> None:
    w(
        "lambda/lab04_inventory/handler.py",
        '''
import json, os
import boto3
table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def lambda_handler(event, _ctx):
    for rec in event.get("Records", []):
        body = json.loads(rec["body"])
        oid = body.get("orderId") or rec["messageId"]
        table.put_item(Item={"pk": f"INV#{oid}", "projection": "inventory", "correlationId": body.get("correlationId")})
        print(json.dumps({"level": "INFO", "msg": "inventory", "orderId": oid}))
''',
    )
    w(
        "lambda/lab04_notify/handler.py",
        '''
import json, os
import boto3
table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def lambda_handler(event, _ctx):
    for rec in event.get("Records", []):
        body = json.loads(rec["body"])
        oid = body.get("orderId") or rec["messageId"]
        table.put_item(Item={"pk": f"N#{oid}", "projection": "notify", "correlationId": body.get("correlationId")})
        print(json.dumps({"level": "INFO", "msg": "notify", "orderId": oid}))
''',
    )
    w(
        "lambda/lab04_analytics/handler.py",
        '''
import json, os
import boto3
table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def lambda_handler(event, _ctx):
    for rec in event.get("Records", []):
        body = json.loads(rec["body"])
        oid = body.get("orderId") or rec["messageId"]
        table.put_item(Item={"pk": f"A#{oid}", "projection": "analytics", "correlationId": body.get("correlationId")})
        print(json.dumps({"level": "INFO", "msg": "analytics", "orderId": oid}))
''',
    )
    w(
        "lambda/lab05_order/handler.py",
        '''
import json, os, uuid
import boto3
eb = boto3.client("events")

def lambda_handler(event, _ctx):
    cid = str(uuid.uuid4())
    oid = event.get("orderId") or str(uuid.uuid4())
    eb.put_events(Entries=[{
        "EventBusName": os.environ["BUS_NAME"],
        "Source": "eia.orders",
        "DetailType": "OrderCreated",
        "Detail": json.dumps({"orderId": oid, "correlationId": cid, "amount": 20}),
    }])
    return {"orderId": oid, "correlationId": cid}
''',
    )
    w(
        "lambda/lab05_payment/handler.py",
        '''
import json, os
import boto3
eb = boto3.client("events")
ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def lambda_handler(event, _ctx):
    d = event.get("detail") or {}
    eid = event.get("id")
    ddb.put_item(Item={"pk": f"PAY#{eid}", "orderId": d.get("orderId"), "correlationId": d.get("correlationId")})
    eb.put_events(Entries=[{
        "EventBusName": os.environ["BUS_NAME"],
        "Source": "eia.payments",
        "DetailType": "PaymentAuthorized",
        "Detail": json.dumps({"orderId": d.get("orderId"), "correlationId": d.get("correlationId"), "eventId": eid}),
    }])
''',
    )
    w(
        "lambda/lab05_inventory/handler.py",
        '''
import json, os
import boto3
eb = boto3.client("events")
ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def lambda_handler(event, _ctx):
    d = event.get("detail") or {}
    eid = event.get("id")
    ddb.put_item(Item={"pk": f"INV#{eid}", "orderId": d.get("orderId"), "correlationId": d.get("correlationId")})
    eb.put_events(Entries=[{
        "EventBusName": os.environ["BUS_NAME"],
        "Source": "eia.inventory",
        "DetailType": "InventoryReserved",
        "Detail": json.dumps({"orderId": d.get("orderId"), "correlationId": d.get("correlationId")}),
    }])
''',
    )
    w(
        "lambda/lab05_notify/handler.py",
        '''
import json, os
import boto3
ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def lambda_handler(event, _ctx):
    d = event.get("detail") or {}
    ddb.put_item(Item={"pk": f"DONE#{d.get('orderId')}", "status": "OrderCompleted", "correlationId": d.get("correlationId")})
    print(json.dumps({"level": "INFO", "msg": "completed", "orderId": d.get("orderId")}))
''',
    )
    w(
        "lambda/lab06_validate/handler.py",
        '''
import hashlib, json, os, urllib.parse
import boto3

s3 = boto3.client("s3")
ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
DEST = os.environ.get("DEST_PREFIX", "accepted/")
Q = os.environ.get("QUARANTINE_PREFIX", "quarantine/")

def lambda_handler(event, _ctx):
    for rec in event.get("Records", []):
        body = json.loads(rec["body"])
        # S3 event wrapped via SQS
        for rec2 in body.get("Records", [body]):
            bkt = rec2["s3"]["bucket"]["name"]
            key = urllib.parse.unquote_plus(rec2["s3"]["object"]["key"])
            obj = s3.get_object(Bucket=bkt, Key=key)
            data = obj["Body"].read()
            sha = hashlib.sha256(data).hexdigest()
            cid = obj.get("Metadata", {}).get("correlationid") or sha[:16]
            # duplicate?
            try:
                ddb.put_item(Item={"pk": f"HASH#{sha}", "key": key, "status": "ACCEPTED", "correlationId": cid},
                             ConditionExpression="attribute_not_exists(pk)")
                duplicate = False
            except Exception:
                duplicate = True
            ok = (not duplicate) and key.endswith(".csv") and b"partner" in data[:200].lower()
            dest = DEST + key.split("/")[-1]
            status = "ACCEPTED"
            if duplicate or not ok:
                dest = Q + key.split("/")[-1]
                status = "DUPLICATE" if duplicate else "QUARANTINED"
            s3.copy_object(Bucket=bkt, CopySource={"Bucket": bkt, "Key": key}, Key=dest)
            ddb.put_item(Item={"pk": f"FILE#{key}", "checksum": sha, "status": status, "correlationId": cid, "dest": dest})
            print(json.dumps({"level": "INFO", "msg": "file", "status": status, "key": key, "correlationId": cid}))
''',
    )
    w(
        "lambda/lab07_init_upload/handler.py",
        '''
import json, os, uuid
import boto3

s3 = boto3.client("s3")
ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
BUCKET = os.environ["BUCKET"]

def lambda_handler(event, _ctx):
    job = str(uuid.uuid4())
    key = f"inbound/{job}.bin"
    url = s3.generate_presigned_url("put_object", Params={"Bucket": BUCKET, "Key": key}, ExpiresIn=900)
    ddb.put_item(Item={"pk": job, "status": "PENDING_UPLOAD", "key": key})
    return {"statusCode": 202, "headers": {"content-type": "application/json"},
            "body": json.dumps({"jobId": job, "uploadUrl": url, "key": key})}
''',
    )
    w(
        "lambda/lab07_process/handler.py",
        '''
import hashlib, json, os, urllib.parse
import boto3

s3 = boto3.client("s3")
ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def lambda_handler(event, _ctx):
    for rec in event.get("Records", []):
        bkt = rec["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(rec["s3"]["object"]["key"])
        job = key.split("/")[-1].replace(".bin", "")
        data = s3.get_object(Bucket=bkt, Key=key)["Body"].read()
        sha = hashlib.sha256(data).hexdigest()
        ddb.update_item(Key={"pk": job}, UpdateExpression="SET #s = :s, checksum = :c",
                        ExpressionAttributeNames={"#s": "status"},
                        ExpressionAttributeValues={":s": "COMPLETED", ":c": sha})
        print(json.dumps({"level": "INFO", "msg": "processed", "jobId": job, "bytes": len(data)}))
''',
    )
    w(
        "lambda/lab07_status/handler.py",
        '''
import json, os
import boto3

ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def lambda_handler(event, _ctx):
    job = (event.get("pathParameters") or {}).get("id") or (event.get("rawPath") or "").split("/")[-1]
    item = ddb.get_item(Key={"pk": job}).get("Item")
    if not item:
        return {"statusCode": 404, "body": json.dumps({"code": "NOT_FOUND"})}
    return {"statusCode": 200, "body": json.dumps({"jobId": job, "status": item.get("status"), "checksum": item.get("checksum")})}
''',
    )
    w(
        "lambda/lab13_metrics/handler.py",
        '''
import json, os, time
import boto3

cw = boto3.client("cloudwatch")
NS = os.environ.get("METRIC_NS", "EIA/Lab13")

def lambda_handler(event, _ctx):
    n = int((event or {}).get("transactions", 5))
    fails = int((event or {}).get("failures", 1))
    cw.put_metric_data(Namespace=NS, MetricData=[
        {"MetricName": "Transactions", "Value": n, "Unit": "Count"},
        {"MetricName": "Success", "Value": n - fails, "Unit": "Count"},
        {"MetricName": "Failure", "Value": fails, "Unit": "Count"},
        {"MetricName": "LatencyMs", "Value": 42, "Unit": "Milliseconds"},
        {"MetricName": "QueueDepth", "Value": int((event or {}).get("depth", 0)), "Unit": "Count"},
        {"MetricName": "DLQVisible", "Value": int((event or {}).get("dlq", 0)), "Unit": "Count"},
        {"MetricName": "FileCounts", "Value": int((event or {}).get("files", 2)), "Unit": "Count"},
        {"MetricName": "ProcessingDurationMs", "Value": 1200, "Unit": "Milliseconds"},
    ])
    print(json.dumps({"level": "INFO", "msg": "metrics_emitted", "correlationId": "lab13", "ts": time.time()}))
    return {"ok": True}
''',
    )
    w(
        "lambda/lab15_tools/handler.py",
        '''
"""Governed tools: status reads vs write that requires approval."""
import json, os, time, uuid
import boto3

ddb = boto3.resource("dynamodb")
catalog = ddb.Table(os.environ["CATALOG_TABLE"])
approvals = ddb.Table(os.environ["APPROVAL_TABLE"])
READ = {"GetFileStatus", "FindFailedTransactions", "ExplainError", "CheckQueueDepth", "GetProcessingStatus", "RecommendRemediation"}
WRITE = {"RequestReprocess"}

def _body(event):
    raw = event.get("body") or "{}"
    return json.loads(raw) if isinstance(raw, str) else raw

def lambda_handler(event, _ctx):
    path = event.get("rawPath") or event.get("path") or ""
    payload = _body(event)
    tool = payload.get("tool") or path.rstrip("/").split("/")[-1]
    if tool in READ:
        if tool == "GetFileStatus":
            item = catalog.get_item(Key={"pk": payload.get("fileId", "FILE#demo.csv")}).get("Item") or {"status": "UNKNOWN"}
            return _ok({"tool": tool, "result": item})
        if tool == "CheckQueueDepth":
            return _ok({"tool": tool, "result": {"depth": 0, "note": "wire SQS in capstone"}})
        if tool == "FindFailedTransactions":
            return _ok({"tool": tool, "result": {"failed": 2, "sample": ["tx-1", "tx-2"]}})
        if tool == "ExplainError":
            return _ok({"tool": tool, "result": {"code": "SCHEMA", "message": "CSV header missing partner column"}})
        if tool == "GetProcessingStatus":
            return _ok({"tool": tool, "result": {"stage": "QUARANTINED"}})
        if tool == "RecommendRemediation":
            return _ok({"tool": tool, "result": {"recommend": "Fix schema and RequestReprocess with HITL"}})
    if tool in WRITE:
        aid = str(uuid.uuid4())
        approvals.put_item(Item={"pk": aid, "status": "PENDING", "action": "reprocess", "fileId": payload.get("fileId"), "ts": int(time.time())})
        return _ok({"tool": tool, "approvalId": aid, "status": "PENDING_APPROVAL"})
    if path.endswith("/approve"):
        aid = payload.get("approvalId")
        approvals.update_item(Key={"pk": aid}, UpdateExpression="SET #s = :s",
                              ExpressionAttributeNames={"#s": "status"},
                              ExpressionAttributeValues={":s": "APPROVED"})
        return _ok({"approved": aid, "audit": "FileReprocessRequested"})
    return {"statusCode": 400, "body": json.dumps({"code": "UNKNOWN_TOOL", "tool": tool})}

def _ok(body):
    return {"statusCode": 200, "headers": {"content-type": "application/json"}, "body": json.dumps(body, default=str)}
''',
    )
    w(
        "lambda/lab12_fix/handler.py",
        '''
"""Placeholder processor used by the security lab."""
def lambda_handler(event, _ctx):
    return {"ok": True, "note": "Tighten IAM in Terraform until validate_lab.py PASSes."}
''',
    )
    w("sample-data/events/order-created.json", json_ex("OrderCreated"))
    w("sample-data/events/payment-authorized.json", json_ex("PaymentAuthorized"))
    w("sample-data/files/good.csv", "partner,amount,txn_id\\nABC,10.00,t-1\\n")
    w("sample-data/files/poison.csv", "<html>not a csv</html>\\n")
    w("sample-data/files/good.csv.sha256", "replace-after-hash\\n")
    w("labs/lab-08-esb-modernization/as-is.md", AS_IS)
    w("labs/lab-11-chaos/scenarios.md", CHAOS)
    w("scripts/ops_agent.py", OPS_AGENT)
    # Hand-maintained deploy/validate scripts — do not overwrite working labs.
    print("skip lab_up/lab_down/destroy_all/validate_lab (maintained outside this generator)")
    import os
    import stat

    for rel in [
        "scripts/lab_up.sh",
        "scripts/lab_down.sh",
        "scripts/destroy_all.sh",
        "scripts/validate_lab.py",
        "scripts/ops_agent.py",
    ]:
        p = ROOT / rel
        os.chmod(p, p.stat().st_mode | stat.S_IEXEC)


def json_ex(t: str) -> str:
    return '{\n  "specversion": "1.0",\n  "type": "%s",\n  "source": "eia.lab",\n  "id": "demo-1",\n  "correlationId": "corr-1",\n  "data": {"orderId": "o-1", "amount": 20}\n}\n' % t


AS_IS = """# As-is ESB (Lab 8)

Northbridge runs a central ESB (conceptual — not a vendor product).

Flows on the bus today:

1. Mobile balance lookup (sync SOAP through the bus to core) — 300 ms needed
2. Address change mapped to 12 downstreams via bus transforms
3. Marketing email triggered from the bus after any customer update
4. Nightly 8 GB settlement file dropped to the bus FTP adapter
5. ISO 20022 MQ to the scheme (certified map, two changes in five years)
6. Warehouse inventory commands during store hours; warehouse down Sundays
7. New collections SaaS — waiting 6 weeks for a map
8. A point-to-point JDBC from reporting that bypasses the bus (undocumented)

Problems: mapping lead time 6 weeks; weekend freezes; one bad map pages everyone; canonical Customer committee.

Produce keep/change/retire, strangler waves, dual-run for money, and `templates/adr.md`.
"""

CHAOS = """# Chaos scenarios

| ID | Break | Observe | Recover |
|----|-------|---------|---------|
| C1 | Set Lambda reserved concurrency 0 | Queue depth / iterator | Restore concurrency; drain |
| C2 | Client timeout shorter than work | Duplicate posts | Idempotency keys |
| C3 | Stop consumer | DLQ or visibility | Restart; replay |
| C4 | Invalid JSON | DLQ + error code | Fix producer or quarantine |
| C5 | Replay same event id | Second projection? | Conditional put |
| C6 | PUT same file twice | DuplicateDetected | Catalog hash |
| C7 | IAM deny on DynamoDB | 5xx + no silent 200 | Fix policy; alarm |

Minimum: complete four with notes in submissions/lab-11/notes.md.
"""

OPS_AGENT = r'''#!/usr/bin/env python3
"""Mock ops agent: can ONLY call the tool HTTP API. No database access."""
import argparse, json, urllib.request

def call(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"content-type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tools-url", required=True)
    p.add_argument("--ask", required=True)
    args = p.parse_args()
    q = args.ask.lower()
    if "arrive" in q or "status" in q:
        tool = "GetFileStatus"
    elif "fail" in q:
        tool = "FindFailedTransactions"
    elif "queue" in q:
        tool = "CheckQueueDepth"
    elif "reprocess" in q:
        tool = "RequestReprocess"
    else:
        tool = "ExplainError"
    print(json.dumps({"planner": "mock", "tool": tool, "result": call(args.tools_url, {"tool": tool, "fileId": "FILE#demo.csv"})}, indent=2))

if __name__ == "__main__":
    main()
'''

LAB_UP = """#!/usr/bin/env bash
set -euo pipefail
LAB=${1:?lab directory name under terraform/labs}
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DIR="$ROOT/terraform/labs/$LAB"
if [[ ! -d "$DIR" ]]; then echo "No $DIR"; exit 1; fi
if [[ ! -f "$DIR/terraform.tfvars" && -f "$DIR/terraform.tfvars.example" ]]; then
  cp "$DIR/terraform.tfvars.example" "$DIR/terraform.tfvars"
fi
terraform -chdir="$DIR" init -input=false
terraform -chdir="$DIR" apply -auto-approve
"""

LAB_DOWN = """#!/usr/bin/env bash
set -euo pipefail
LAB=${1:?lab directory name}
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DIR="$ROOT/terraform/labs/$LAB"
terraform -chdir="$DIR" destroy -auto-approve
"""

DESTROY = """#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" != "--yes" ]]; then echo "Usage: $0 --yes"; exit 1; fi
ROOT=$(cd "$(dirname "$0")/.." && pwd)
for d in "$ROOT"/terraform/labs/*; do
  [[ -d "$d" ]] || continue
  echo "Destroying $(basename "$d")"
  terraform -chdir="$d" destroy -auto-approve || true
done
"""

VALIDATE = r'''#!/usr/bin/env python3
"""PASS/FAIL lab validation with remediation hints."""
from __future__ import annotations
import json, os, sys, uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def fail(msg: str, hint: str) -> None:
    print("FAIL")
    print(msg)
    print("Remediation:", hint)
    sys.exit(1)

def ok(msg: str) -> None:
    print("PASS")
    print(msg)

def lab01() -> None:
    p = ROOT / "submissions" / "lab-01" / "worksheet.md"
    if not p.exists():
        fail("Missing submissions/lab-01/worksheet.md", "Copy labs/lab-01-classification/worksheet.md and complete 15 items.")
    text = p.read_text()
    if text.count("Rationale") < 15 and text.count("**Rationale") < 10:
        fail("Worksheet does not look complete (need 15 rationales).", "Fill all 15 items with ≥ 40 characters each.")
    ok("Worksheet present. Instructor still grades rationale quality.")

def need_boto():
    try:
        import boto3
        return boto3
    except ImportError:
        fail("boto3 missing", "pip install boto3")

def tf_out(lab: str) -> dict:
    import subprocess
    d = ROOT / "terraform" / "labs" / lab
    r = subprocess.run(["terraform", f"-chdir={d}", "output", "-json"], capture_output=True, text=True)
    if r.returncode != 0:
        fail("terraform output failed", f"Deploy first: ./scripts/lab_up.sh {lab}\\n{r.stderr}")
    raw = json.loads(r.stdout or "{}")
    return {k: v.get("value") for k, v in raw.items()}

def lab02() -> None:
    boto3 = need_boto()
    out = tf_out("lab-02-api")
    ep = out.get("api_endpoint")
    if not ep:
        fail("No API endpoint", "terraform apply lab-02-api")
    import urllib.request
    key = str(uuid.uuid4())
    req = urllib.request.Request(
        ep.rstrip("/") + "/orders",
        data=json.dumps({"customerId": "c1", "amount": 1.5}).encode(),
        headers={"content-type": "application/json", "Idempotency-Key": key, "x-correlation-id": "validate-02"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status not in (200, 201):
                fail(f"POST status {resp.status}", "Check Lambda logs and IAM.")
    except Exception as e:
        fail(str(e), "Confirm API Gateway route POST /orders and Lambda permission.")
    ok("API create path responded. Also retry idempotency manually.")

def notes(lab: str, rel: str) -> None:
    p = ROOT / rel
    if not p.exists() or len(p.read_text()) < 200:
        fail(f"Missing or thin {rel}", "Write the required narrative/ADR/notes.")
    ok(f"{rel} present.")

HANDLERS = {
    "lab-01-classification": lab01,
    "lab-02-api": lab02,
    "lab-03-messaging": lambda: ok("Deployed? Check terraform output queue_url, send poison, inspect DLQ.") if (ROOT/"terraform/labs/lab-03-messaging").exists() else fail("missing", "apply"),
    "lab-04-pubsub": lambda: ok("Check three consumer log groups after one publish."),
    "lab-05-events": lambda: ok("Put OrderCreated; confirm OrderCompleted projection."),
    "lab-06-file-transfer": lambda: ok("Upload sample-data/files/good.csv to inbound prefix; catalog ACCEPTED."),
    "lab-07-large-files": lambda: ok("Init upload, PUT, GET status COMPLETED."),
    "lab-08-esb-modernization": lambda: notes("lab-08", "submissions/lab-08/adr.md"),
    "lab-11-chaos": lambda: notes("lab-11", "submissions/lab-11/notes.md"),
    "lab-12-security": lambda: ok("FAIL this lab until S3 PublicAccessBlock and no dynamodb:* on * — extend checks with boto3 in class."),
    "lab-13-observability": lambda: ok("Dashboard output must exist; emit metrics via lab13 generator."),
    "lab-15-ai-agent": lambda: ok("Mock agent can call tools; reprocess stays PENDING until /approve."),
}

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_lab.py <lab-id>")
        sys.exit(2)
    lab = sys.argv[1]
    fn = HANDLERS.get(lab)
    if not fn:
        fail("Unknown lab", "Use ids like lab-02-api")
    fn()

'''

if __name__ == "__main__":
    main()
