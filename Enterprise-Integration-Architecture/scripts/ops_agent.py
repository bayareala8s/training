#!/usr/bin/env python3
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
