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
