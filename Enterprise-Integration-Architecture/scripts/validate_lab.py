#!/usr/bin/env python3
"""PASS/FAIL validation for labs and capstones. Hits deployed AWS stacks (except paper labs)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOW_SAMPLES = os.environ.get("EIA_ALLOW_SAMPLES") == "1"


def fail(msg: str, hint: str) -> None:
    print("FAIL")
    print(msg)
    print("Remediation:", hint)
    sys.exit(1)


def ok(msg: str) -> None:
    print("PASS")
    print(msg)


def need_boto():
    try:
        import boto3  # noqa: F401

        return boto3
    except ImportError:
        fail("boto3 missing", "pip install boto3")


def tf_dir(lab: str) -> Path:
    p = ROOT / "terraform" / "labs" / lab
    if p.is_dir():
        return p
    p = ROOT / "terraform" / "capstones" / lab
    if p.is_dir():
        return p
    fail(f"No terraform directory for {lab}", "Use an id under terraform/labs or terraform/capstones.")


def tf_out(lab: str) -> dict:
    d = tf_dir(lab)
    r = subprocess.run(["terraform", f"-chdir={d}", "output", "-json"], capture_output=True, text=True)
    if r.returncode != 0:
        fail("terraform output failed", f"Deploy first: ./scripts/lab_up.sh {lab}\n{r.stderr}")
    raw = json.loads(r.stdout or "{}")
    return {k: v.get("value") for k, v in raw.items()}


def http_json(method: str, url: str, body=None, headers=None, timeout=20):
    headers = {"content-type": "application/json", **(headers or {})}
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode()
            parsed = json.loads(raw) if raw else {}
            return resp.status, parsed
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = {"raw": raw}
        return e.code, parsed
    except Exception as e:
        fail(str(e), f"HTTP {method} {url} failed. Check deploy, routes, and Lambda logs.")


def wait_until(fn, timeout=90, interval=2, hint="Check Lambda logs, IAM, and event source mappings."):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        last = fn()
        if last:
            return last
        time.sleep(interval)
    fail(f"Timed out after {timeout}s waiting for a condition.", hint)


def ddb_item(table: str, pk: str, region: str):
    boto3 = need_boto()
    item = boto3.resource("dynamodb", region_name=region).Table(table).get_item(Key={"pk": pk}).get("Item")
    return item


def notes(rel: str, min_len: int = 200) -> None:
    p = ROOT / rel
    if not p.exists() or len(p.read_text()) < min_len:
        fail(f"Missing or thin {rel}", f"Write the required narrative at {rel}.")


def lab01() -> None:
    p = ROOT / "submissions" / "lab-01" / "worksheet.md"
    if not p.exists():
        fail(
            "Missing submissions/lab-01/worksheet.md",
            "Copy labs/lab-01-classification/worksheet.md and complete 15 items.",
        )
    text = p.read_text()
    if not ALLOW_SAMPLES and ("Instructor sample only" in text or "instructor smoke test" in text.lower()):
        fail(
            "submissions/lab-01/worksheet.md looks like the instructor sample.",
            "Copy labs/lab-01-classification/worksheet.md and write your own 15 rationales.",
        )
    if text.count("Rationale") < 15 and text.count("**Rationale") < 10:
        fail("Worksheet does not look complete (need 15 rationales).", "Fill all 15 items with ≥ 40 characters each.")
    ok("Worksheet present with 15 rationale markers. Instructor still grades rationale quality.")


def lab02() -> None:
    out = tf_out("lab-02-api")
    ep = (out.get("api_endpoint") or "").rstrip("/")
    if not ep:
        fail("No API endpoint", "./scripts/lab_up.sh lab-02-api")
    key = str(uuid.uuid4())
    status, body = http_json(
        "POST",
        ep + "/orders",
        {"customerId": "c1", "amount": 1.5},
        {"Idempotency-Key": key, "x-correlation-id": "validate-02"},
    )
    if status not in (200, 201) or not body.get("orderId"):
        fail(f"POST /orders returned {status} {body}", "Check Lambda logs, IAM, and Idempotency-Key handling.")
    oid = body["orderId"]
    st2, replay = http_json(
        "POST",
        ep + "/orders",
        {"customerId": "c1", "amount": 1.5},
        {"Idempotency-Key": key, "x-correlation-id": "validate-02-replay"},
    )
    if st2 != 200 or replay.get("orderId") != oid:
        fail(f"Idempotent replay failed: {st2} {replay}", "Conditional PutItem on IDEM#key must return the original orderId.")
    st3, got = http_json("GET", ep + f"/orders/{oid}", headers={"x-correlation-id": "validate-02-get"})
    if st3 != 200 or (got.get("order") or {}).get("orderId") != oid:
        fail(f"GET /orders/{{id}} failed: {st3} {got}", "Query the orderId GSI instead of Scan with Limit.")
    st4, _ = http_json("POST", ep + "/orders", {"customerId": "c1", "amount": 1.5})
    if st4 != 400:
        fail(f"Missing Idempotency-Key should be 400, got {st4}", "Reject POSTs without Idempotency-Key.")
    ok(f"POST/GET/idempotency work. orderId={oid}")


def lab03() -> None:
    boto3 = need_boto()
    out = tf_out("lab-03-messaging")
    region = out.get("aws_region") or "us-west-2"
    sqs = boto3.client("sqs", region_name=region)
    table = out["table_name"]
    body = {"paymentId": str(uuid.uuid4()), "correlationId": "validate-03", "amount": 10.0}
    sent = sqs.send_message(QueueUrl=out["queue_url"], MessageBody=json.dumps(body))
    mid = sent["MessageId"]
    wait_until(
        lambda: (ddb_item(table, f"MSG#{mid}", region) or {}).get("status") == "POSTED",
        timeout=60,
        hint="Consumer must PutItem MSG#{messageId} with status POSTED.",
    )
    sqs.send_message(QueueUrl=out["queue_url"], MessageBody=json.dumps({"amount": "POISON", "correlationId": "validate-03-poison"}))

    def dlq_has_msg():
        attrs = sqs.get_queue_attributes(QueueUrl=out["dlq_url"], AttributeNames=["ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible"])
        n = int(attrs["Attributes"].get("ApproximateNumberOfMessages", 0)) + int(attrs["Attributes"].get("ApproximateNumberOfMessagesNotVisible", 0))
        return n >= 1

    wait_until(dlq_has_msg, timeout=45, hint="Poison (amount=POISON) must raise so SQS redrive sends the message to the DLQ (maxReceiveCount=2, visibility 10s).")
    ok("Good message posted; poison landed on the DLQ.")


def lab04() -> None:
    boto3 = need_boto()
    out = tf_out("lab-04-pubsub")
    region = out.get("aws_region") or "us-west-2"
    oid = str(uuid.uuid4())
    boto3.client("sns", region_name=region).publish(
        TopicArn=out["topic_arn"],
        Message=json.dumps({"orderId": oid, "correlationId": "validate-04"}),
    )
    table = out["table_name"]
    wait_until(lambda: ddb_item(table, f"INV#{oid}", region), timeout=60, hint="Unwrap SNS Message JSON; project INV#{orderId}.")
    wait_until(lambda: ddb_item(table, f"N#{oid}", region), timeout=30, hint="Notify consumer must unwrap SNS envelopes.")
    wait_until(lambda: ddb_item(table, f"A#{oid}", region), timeout=30, hint="Analytics consumer must unwrap SNS envelopes.")
    ok(f"One publish projected inventory, notify, and analytics for orderId={oid}.")


def lab05() -> None:
    boto3 = need_boto()
    out = tf_out("lab-05-events")
    region = out.get("aws_region") or "us-west-2"
    oid = str(uuid.uuid4())
    ep = (out.get("api_endpoint") or "").rstrip("/")
    if ep:
        st, body = http_json("POST", ep + "/orders", {"orderId": oid, "correlationId": "validate-05", "amount": 20})
        if st not in (200, 202) or body.get("orderId") != oid:
            fail(f"POST /orders failed: {st} {body}", "Wire lab05_order to POST /orders and PutEvents OrderCreated.")
    else:
        boto3.client("lambda", region_name=region).invoke(
            FunctionName=out["order_function"],
            Payload=json.dumps({"orderId": oid, "correlationId": "validate-05"}).encode(),
        )
    wait_until(
        lambda: (ddb_item(out["table_name"], f"DONE#{oid}", region) or {}).get("status") == "OrderCompleted",
        timeout=90,
        hint="OrderCreated → PaymentAuthorized → InventoryReserved → DONE#{orderId}. Confirm EventBridge rules and put_events permissions.",
    )
    ok(f"Choreography completed OrderCompleted for {oid}.")


def lab06() -> None:
    boto3 = need_boto()
    out = tf_out("lab-06-file-transfer")
    region = out.get("aws_region") or "us-west-2"
    s3 = boto3.client("s3", region_name=region)
    bucket = out["bucket"]
    table = out["table_name"]
    good = (ROOT / "sample-data" / "files" / "good.csv").read_bytes()
    poison = (ROOT / "sample-data" / "files" / "poison.csv").read_bytes()
    s3.put_object(Bucket=bucket, Key="inbound/good.csv", Body=good)
    wait_until(
        lambda: (ddb_item(table, "FILE#inbound/good.csv", region) or {}).get("status") == "ACCEPTED",
        timeout=90,
        hint="Validator must ACCEPTED CSV files that contain a partner column.",
    )
    s3.put_object(Bucket=bucket, Key="inbound/poison.csv", Body=poison)
    wait_until(
        lambda: (ddb_item(table, "FILE#inbound/poison.csv", region) or {}).get("status") == "QUARANTINED",
        timeout=90,
        hint="Non-CSV / missing partner header must QUARANTINED, not ACCEPTED.",
    )
    s3.put_object(Bucket=bucket, Key="inbound/good-dup.csv", Body=good)
    wait_until(
        lambda: (ddb_item(table, "FILE#inbound/good-dup.csv", region) or {}).get("status") == "DUPLICATE",
        timeout=90,
        hint="Same SHA-256 as an ACCEPTED file must be DUPLICATE (GetItem HASH# before PutItem).",
    )
    ok("Accepted good.csv, quarantined poison.csv, detected duplicate hash.")


def lab07() -> None:
    out = tf_out("lab-07-large-files")
    ep = (out.get("api_endpoint") or "").rstrip("/")
    st, body = http_json("POST", ep + "/uploads", {}, {"x-correlation-id": "validate-07"})
    if st not in (200, 202) or not body.get("jobId") or not body.get("uploadUrl"):
        fail(f"Init upload failed: {st} {body}", "POST /uploads must return jobId and uploadUrl.")
    job = body["jobId"]
    req = urllib.request.Request(body["uploadUrl"], data=b"claim-check-bytes", method="PUT")
    try:
        urllib.request.urlopen(req, timeout=30).read()
    except Exception as e:
        fail(str(e), "Presigned PUT must succeed against the lab bucket.")
    wait_until(
        lambda: http_json("GET", ep + f"/uploads/{job}")[1].get("status") == "COMPLETED",
        timeout=90,
        hint="S3 ObjectCreated on inbound/ must process the object and set job status COMPLETED.",
    )
    ok(f"Upload job {job} reached COMPLETED.")


def lab08() -> None:
    notes("submissions/lab-08/adr.md", 400)
    text = (ROOT / "submissions" / "lab-08" / "adr.md").read_text()
    if not ALLOW_SAMPLES and "Reference ADR for instructors" in text:
        fail(
            "ADR is the instructor reference, not your decision.",
            "Write submissions/lab-08/adr.md from templates/adr.md and as-is.md.",
        )
    required = ["Business Problem", "Options Considered", "Decision", "Rationale", "Tradeoffs", "Security Impact", "Reliability Impact", "Cost Impact"]
    missing = [h for h in required if h.lower() not in text.lower()]
    if missing:
        fail(f"ADR missing sections: {missing}", "Use templates/adr.md. See labs/lab-08-esb-modernization/reference/adr.md.")
    demo = ROOT / "labs" / "lab-08-esb-modernization" / "strangler_demo.py"
    r = subprocess.run([sys.executable, str(demo)], capture_output=True, text=True)
    if r.returncode != 0:
        fail("strangler_demo.py failed", r.stdout + r.stderr)
    d = ROOT / "terraform" / "labs" / "lab-08-esb-modernization"
    probe = subprocess.run(["terraform", f"-chdir={d}", "output", "-json"], capture_output=True, text=True)
    if probe.returncode == 0:
        raw = json.loads(probe.stdout or "{}")
        ep = (raw.get("api_endpoint") or {}).get("value")
        if ep:
            st, body = http_json("GET", str(ep).rstrip("/") + "/balances/demo")
            if st != 200 or not body.get("notViaEsb"):
                fail(f"Optional façade GET failed: {st} {body}", "GET /balances/{id} is the strangler slice.")
    ok("ADR complete and local strangler router passes. Optional AWS façade checked if deployed.")


def lab11() -> None:
    notes("submissions/lab-11/notes.md", 300)
    text = (ROOT / "submissions" / "lab-11" / "notes.md").read_text()
    if not ALLOW_SAMPLES and "Students replace this with their own evidence" in text:
        fail(
            "Notes still look like labs/lab-11-chaos/sample-notes.md.",
            "Write your own observations for at least four of C1–C7.",
        )
    hits = sum(1 for code in ["C1", "C2", "C3", "C4", "C5", "C6", "C7"] if code in text)
    if hits < 4:
        fail("Notes must cover at least four chaos scenario IDs (C1–C7).", "See labs/lab-11-chaos/scenarios.md.")
    boto3 = need_boto()
    out = tf_out("lab-11-chaos")
    region = out.get("aws_region") or "us-west-2"
    sqs = boto3.client("sqs", region_name=region)
    sent = sqs.send_message(QueueUrl=out["queue_url"], MessageBody=json.dumps({"paymentId": str(uuid.uuid4()), "amount": 5, "correlationId": "c-ok"}))
    wait_until(
        lambda: (ddb_item(out["table_name"], f"MSG#{sent['MessageId']}", region) or {}).get("status") == "POSTED",
        timeout=60,
        hint="Deploy lab-11-chaos and confirm the consumer posts good messages.",
    )
    sqs.send_message(QueueUrl=out["queue_url"], MessageBody=json.dumps({"amount": "POISON"}))
    sqs.send_message(QueueUrl=out["queue_url"], MessageBody="not-json")

    def dlq_ready():
        attrs = sqs.get_queue_attributes(QueueUrl=out["dlq_url"], AttributeNames=["ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible"])
        n = int(attrs["Attributes"].get("ApproximateNumberOfMessages", 0)) + int(attrs["Attributes"].get("ApproximateNumberOfMessagesNotVisible", 0))
        return n >= 2

    wait_until(dlq_ready, timeout=50, hint="Poison and invalid JSON must land on the DLQ.")
    ok("Notes cover ≥4 scenarios; chaos stack posted a good message and DLQ received poison + invalid JSON.")


def lab12() -> None:
    boto3 = need_boto()
    out = tf_out("lab-12-security")
    region = out.get("aws_region") or "us-west-2"
    if out.get("insecure") is True:
        fail(
            "Stack is still deployed with insecure=true (star IAM and public-access block disabled).",
            "Set insecure=false in terraform/labs/lab-12-security/terraform.tfvars and re-apply.",
        )
    s3 = boto3.client("s3", region_name=region)
    pab = s3.get_public_access_block(Bucket=out["bucket"])["PublicAccessBlockConfiguration"]
    if not all(pab.get(k) for k in ("BlockPublicAcls", "BlockPublicPolicy", "IgnorePublicAcls", "RestrictPublicBuckets")):
        fail(f"S3 public access block is incomplete: {pab}", "Enable all four PublicAccessBlock flags.")
    iam = boto3.client("iam", region_name=region)
    role = out.get("function_role_name")
    if role:
        for name in iam.list_role_policies(RoleName=role).get("PolicyNames") or []:
            doc = iam.get_role_policy(RoleName=role, PolicyName=name)["PolicyDocument"]
            blob = json.dumps(doc)
            if "dynamodb:*" in blob or "s3:*" in blob:
                fail("IAM still allows dynamodb:* or s3:* on *.", "Scope DynamoDB/S3 to the lab table and /allowed/* prefix.")
    ok("insecure=false, public access blocked, IAM no longer uses dynamodb:* on *.")


def lab13() -> None:
    boto3 = need_boto()
    out = tf_out("lab-13-observability")
    region = out.get("aws_region") or "us-west-2"
    resp = boto3.client("lambda", region_name=region).invoke(
        FunctionName=out["function_name"],
        Payload=json.dumps({"transactions": 5, "failures": 1, "depth": 2, "dlq": 1, "files": 3}).encode(),
    )
    payload = json.loads(resp["Payload"].read().decode() or "{}")
    if resp.get("FunctionError") or not payload.get("ok"):
        fail(f"Metrics lambda failed: {payload}", "Confirm cloudwatch:PutMetricData and invoke the generator.")
    dash = boto3.client("cloudwatch", region_name=region).get_dashboard(DashboardName=out["dashboard_name"])
    if "Transactions" not in dash.get("DashboardBody", ""):
        fail("Dashboard missing Transactions widget.", "Keep the Lab 13 dashboard widgets.")
    ok(f"Metrics emitted; dashboard {out['dashboard_name']} exists.")


def lab15() -> None:
    out = tf_out("lab-15-ai-agent")
    tools = out["tools_url"]
    approve = out["approve_url"]
    st, before = http_json("POST", tools, {"tool": "GetFileStatus", "fileId": "FILE#demo.csv"})
    if st != 200 or not (before.get("result") or {}).get("status"):
        fail(f"GetFileStatus failed: {st} {before}", "Demo catalog item FILE#demo.csv must exist.")
    status_before = before["result"]["status"]
    st, req = http_json("POST", tools, {"tool": "RequestReprocess", "fileId": "FILE#demo.csv"})
    if st != 200 or req.get("status") != "PENDING_APPROVAL" or not req.get("approvalId"):
        fail(f"RequestReprocess must stay PENDING: {st} {req}", "Writes create an approval row; they must not update the catalog yet.")
    st, mid = http_json("POST", tools, {"tool": "GetFileStatus", "fileId": "FILE#demo.csv"})
    if (mid.get("result") or {}).get("status") != status_before:
        fail("Catalog changed before /approve.", "HITL: only POST /approve may execute the write.")
    st, appr = http_json("POST", approve, {"approvalId": req["approvalId"]})
    if st != 200 or appr.get("status") != "REPROCESSED":
        fail(f"/approve did not reprocess: {st} {appr}", "Approve must update catalog status to REPROCESSED and write an audit field.")
    st, done = http_json("POST", tools, {"tool": "GetFileStatus", "fileId": "FILE#demo.csv"})
    if (done.get("result") or {}).get("status") != "REPROCESSED":
        fail(f"Catalog not REPROCESSED after approve: {done}", "Approve handler must UpdateItem the catalog.")
    st, denied = http_json("POST", tools, {"tool": "DropTable"})
    if st not in (400, 403):
        fail(f"Unknown tool should be rejected, got {st}", "Allow-list tools only.")
    ok("Reads work; reprocess stays PENDING until /approve actually updates the catalog.")


def cap_banking() -> None:
    boto3 = need_boto()
    out = tf_out("banking")
    region = out.get("aws_region") or "us-west-2"
    ep = out["api_endpoint"].rstrip("/")
    key = str(uuid.uuid4())
    st, body = http_json("POST", ep + "/payments", {"customerId": "ABC", "amount": 25}, {"Idempotency-Key": key, "x-correlation-id": "bank-val"})
    if st not in (200, 202) or not body.get("paymentId"):
        fail(f"POST /payments failed: {st} {body}", "./scripts/lab_up.sh banking")
    pid = body["paymentId"]
    wait_until(
        lambda: (ddb_item(out["payments_table"], f"PAY#{pid}", region) or {}).get("status") == "POSTED",
        timeout=60,
        hint="SQS poster must mark PAY#{id} POSTED.",
    )
    s3 = boto3.client("s3", region_name=region)
    s3.put_object(Bucket=out["bucket"], Key="inbound/good.csv", Body=(ROOT / "sample-data" / "files" / "good.csv").read_bytes())
    wait_until(
        lambda: (ddb_item(out["catalog_table"], "FILE#inbound/good.csv", region) or {}).get("status") == "ACCEPTED",
        timeout=90,
        hint="File pipeline must catalog inbound/good.csv as ACCEPTED.",
    )
    st, t = http_json("POST", ep + "/tools", {"tool": "GetFileStatus", "fileId": "FILE#inbound/good.csv"})
    if st != 200:
        fail(f"GetFileStatus failed: {st} {t}", "Ops tools must call GetItem, not Scan *.")
    s3.put_object(Bucket=out["bucket"], Key="inbound/poison.csv", Body=(ROOT / "sample-data" / "files" / "poison.csv").read_bytes())
    wait_until(
        lambda: (ddb_item(out["catalog_table"], "FILE#inbound/poison.csv", region) or {}).get("status") == "QUARANTINED",
        timeout=90,
        hint="Poison files must quarantine.",
    )
    st, req = http_json("POST", ep + "/tools", {"tool": "RequestReprocess", "fileId": "FILE#inbound/poison.csv"})
    st, ap = http_json("POST", ep + "/approve", {"approvalId": req.get("approvalId")})
    if ap.get("status") != "REPROCESSED":
        fail(f"HITL approve failed: {st} {ap}", "POST /approve is the only write path.")
    ok("Banking slice: idempotent payment posted, file catalogued, HITL reprocess audited.")


def cap_ecommerce() -> None:
    out = tf_out("ecommerce")
    ep = out["api_endpoint"].rstrip("/")
    st, ok_order = http_json("POST", ep + "/orders", {"amount": 20, "sku": "SKU-1"}, {"x-correlation-id": "ecom-ok"})
    if st not in (200, 202) or not ok_order.get("orderId"):
        fail(f"Happy-path order failed: {st} {ok_order}", "./scripts/lab_up.sh ecommerce")
    oid = ok_order["orderId"]
    wait_until(lambda: http_json("GET", ep + f"/orders/{oid}")[1].get("order", {}).get("status") == "COMPLETED", timeout=90, hint="Saga must complete when inventory reserves.")
    st, bad = http_json("POST", ep + "/orders", {"amount": 13.13, "failInventory": True}, {"x-correlation-id": "ecom-fail"})
    bid = bad.get("orderId")
    wait_until(
        lambda: http_json("GET", ep + f"/orders/{bid}")[1].get("order", {}).get("status") == "COMPENSATED",
        timeout=90,
        hint="When payment succeeds and inventory fails, compensate (VOID payment) — do not leave AUTHORIZED forever.",
    )
    st, tool = http_json("POST", ep + "/tools", {"tool": "GetOrderStatus", "orderId": bid})
    if st != 200:
        fail(f"GetOrderStatus failed: {tool}", "Agent tools must use the order status API.")
    ok("Happy path COMPLETED; payment-ok/inventory-fail COMPENSATED.")


def cap_healthcare() -> None:
    out = tf_out("healthcare")
    ep = out["api_endpoint"].rstrip("/")
    st, clinician = http_json("GET", ep + "/patients/pt-1", headers={"x-actor-role": "clinician", "x-actor-id": "clin-1"})
    if st != 200 or not (clinician.get("patient") or {}).get("patientId"):
        fail(f"Clinician GET failed: {st} {clinician}", "GET /patients/{{id}} is the authorized service.")
    st, forbidden = http_json("GET", ep + "/patients/pt-1", headers={"x-actor-role": "patient", "x-actor-id": "pt-2"})
    if st != 403:
        fail(f"Patient reading another record should be 403, got {st}", "Enforce patient=self.")
    st, tool = http_json("POST", ep + "/tools", {"tool": "GetPatientSummary", "patientId": "pt-1", "actorRole": "clinician", "actorId": "clin-1"})
    if st != 200 or tool.get("via") != "authorized-api":
        fail(f"Agent tool must call the API: {st} {tool}", "Tools Lambda has no DynamoDB policy — it HTTP GETs /patients/{id}.")
    st, denied = http_json("POST", ep + "/tools", {"tool": "ScanAllPatients"})
    if st != 403:
        fail(f"Denied tool should be 403, got {st} {denied}", "List ScanAllPatients as a denied tool.")
    ok("Authorized patient API works; agent tools call the API; ScanAllPatients is denied.")


def cap_manufacturing() -> None:
    boto3 = need_boto()
    out = tf_out("manufacturing")
    region = out.get("aws_region") or "us-west-2"
    ep = out["api_endpoint"].rstrip("/")
    st, missing = http_json("GET", ep + "/suppliers/missing")
    if st != 200 or "ACME" not in (missing.get("missing") or []) or "BOLTCO" not in (missing.get("missing") or []):
        fail(f"All expected suppliers should start missing: {missing}", "Seed expected ACME,BOLTCO,YIELD with no arrivals.")
    boto3.client("s3", region_name=region).put_object(
        Bucket=out["bucket"],
        Key="inbound/ACME/daily.csv",
        Body=b"partner,qty\nACME,10\n",
    )
    wait_until(
        lambda: "ACME" not in (http_json("GET", ep + "/suppliers/missing")[1].get("missing") or []),
        timeout=90,
        hint="Uploading inbound/ACME/daily.csv must clear ACME from missing.",
    )
    st, ship = http_json("GET", ep + "/shipments/92841")
    if st != 200 or (ship.get("shipment") or {}).get("status") != "DELAYED":
        fail(f"Shipment 92841 should be DELAYED: {ship}", "Seed SHIP#92841.")
    st, req = http_json("POST", ep + "/tools", {"tool": "RequestRetry", "supplier": "BOLTCO"})
    st, ap = http_json("POST", ep + "/approve", {"approvalId": req.get("approvalId")})
    if ap.get("status") != "RETRY_REQUESTED":
        fail(f"HITL retry failed: {ap}", "Approve must write RETRY#supplier REQUESTED.")
    ok("Missing-supplier query, ACME arrival, delayed shipment, HITL retry all work.")


HANDLERS = {
    "lab-01-classification": lab01,
    "lab-02-api": lab02,
    "lab-03-messaging": lab03,
    "lab-04-pubsub": lab04,
    "lab-05-events": lab05,
    "lab-06-file-transfer": lab06,
    "lab-07-large-files": lab07,
    "lab-08-esb-modernization": lab08,
    "lab-11-chaos": lab11,
    "lab-12-security": lab12,
    "lab-13-observability": lab13,
    "lab-15-ai-agent": lab15,
    "banking": cap_banking,
    "ecommerce": cap_ecommerce,
    "healthcare": cap_healthcare,
    "manufacturing": cap_manufacturing,
    "capstone-banking": cap_banking,
    "capstone-ecommerce": cap_ecommerce,
    "capstone-healthcare": cap_healthcare,
    "capstone-manufacturing": cap_manufacturing,
}


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_lab.py <lab-id|banking|ecommerce|healthcare|manufacturing>")
        print("Known:", ", ".join(sorted(set(HANDLERS))))
        sys.exit(2)
    lab = sys.argv[1]
    fn = HANDLERS.get(lab)
    if not fn:
        fail("Unknown lab", "Use ids like lab-02-api or banking")
    fn()


if __name__ == "__main__":
    main()
