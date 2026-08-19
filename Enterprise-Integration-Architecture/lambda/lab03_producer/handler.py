"""Send a command to the lab-03 queue. Usage: python handler.py --queue-url URL [--poison]"""

from __future__ import annotations

import argparse
import json
import uuid

import boto3


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--queue-url", required=True)
    p.add_argument("--poison", action="store_true")
    p.add_argument("--region", default="us-west-2")
    args = p.parse_args()
    body = {
        "paymentId": str(uuid.uuid4()),
        "correlationId": str(uuid.uuid4()),
        "amount": "POISON" if args.poison else 10.0,
    }
    boto3.client("sqs", region_name=args.region).send_message(QueueUrl=args.queue_url, MessageBody=json.dumps(body))
    print(json.dumps({"sent": body}))


if __name__ == "__main__":
    main()
