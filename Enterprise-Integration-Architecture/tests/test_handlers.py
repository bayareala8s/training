"""Handler tests that do not require a live AWS account."""

from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path

import boto3
import pytest
from moto import mock_aws

ROOT = Path(__file__).resolve().parents[1]


def _load(folder: str):
    path = ROOT / "lambda" / folder
    sys.path.insert(0, str(path))
    if "handler" in sys.modules:
        del sys.modules["handler"]
    return importlib.import_module("handler")


def _create_table(name: str, gsi=False):
    client = boto3.client("dynamodb", region_name="us-west-2")
    attrs = [{"AttributeName": "pk", "AttributeType": "S"}]
    kwargs = {
        "TableName": name,
        "KeySchema": [{"AttributeName": "pk", "KeyType": "HASH"}],
        "AttributeDefinitions": attrs,
        "BillingMode": "PAY_PER_REQUEST",
    }
    if gsi:
        kwargs["AttributeDefinitions"].append({"AttributeName": "orderId", "AttributeType": "S"})
        kwargs["GlobalSecondaryIndexes"] = [
            {
                "IndexName": "orderId-index",
                "KeySchema": [{"AttributeName": "orderId", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            }
        ]
    client.create_table(**kwargs)
    client.get_waiter("table_exists").wait(TableName=name)


def test_unwrap_sns_envelope():
    from eia_common import unwrap_sqs_body

    inner = {"orderId": "o-1", "correlationId": "c"}
    envelope = json.dumps({"Type": "Notification", "TopicArn": "arn:aws:sns:us-west-2:1:t", "Message": json.dumps(inner)})
    assert unwrap_sqs_body(envelope)["orderId"] == "o-1"
    assert unwrap_sqs_body(json.dumps(inner))["orderId"] == "o-1"


def test_event_detail_string_or_dict():
    from eia_common import event_detail

    assert event_detail({"detail": {"orderId": "x"}})["orderId"] == "x"
    assert event_detail({"detail": json.dumps({"orderId": "y"})})["orderId"] == "y"


@mock_aws
def test_lab02_create_get_idempotent():
    os.environ["TABLE_NAME"] = "orders"
    _create_table("orders", gsi=True)
    h = _load("lab02_orders")
    event = {
        "requestContext": {"http": {"method": "POST"}},
        "rawPath": "/orders",
        "headers": {"Idempotency-Key": "k1", "x-correlation-id": "c1"},
        "body": json.dumps({"customerId": "c1", "amount": 2.5}),
    }
    created = json.loads(h.lambda_handler(event, None)["body"])
    assert created["code"] == "CREATED"
    replay = json.loads(h.lambda_handler(event, None)["body"])
    assert replay["code"] == "REPLAY"
    assert replay["orderId"] == created["orderId"]
    got = json.loads(
        h.lambda_handler(
            {
                "requestContext": {"http": {"method": "GET"}},
                "rawPath": f"/orders/{created['orderId']}",
                "pathParameters": {"id": created["orderId"]},
                "headers": {},
            },
            None,
        )["body"]
    )
    assert got["order"]["orderId"] == created["orderId"]


@mock_aws
def test_lab04_unwraps_sns_and_projects():
    os.environ["TABLE_NAME"] = "proj"
    _create_table("proj")
    h = _load("lab04_inventory")
    inner = {"orderId": "ord-9", "correlationId": "cid"}
    event = {
        "Records": [
            {
                "messageId": "m1",
                "body": json.dumps({"Type": "Notification", "TopicArn": "arn:sns", "Message": json.dumps(inner)}),
            }
        ]
    }
    h.lambda_handler(event, None)
    item = boto3.resource("dynamodb").Table("proj").get_item(Key={"pk": "INV#ord-9"}).get("Item")
    assert item["projection"] == "inventory"


@mock_aws
def test_lab06_quarantine_and_duplicate():
    os.environ["TABLE_NAME"] = "cat"
    _create_table("cat")
    s3 = boto3.client("s3", region_name="us-west-2")
    s3.create_bucket(Bucket="land", CreateBucketConfiguration={"LocationConstraint": "us-west-2"})
    h = _load("lab06_validate")

    def s3_event(key: str):
        return {
            "Records": [
                {
                    "body": json.dumps(
                        {
                            "Records": [
                                {"s3": {"bucket": {"name": "land"}, "object": {"key": key}}}
                            ]
                        }
                    )
                }
            ]
        }

    s3.put_object(Bucket="land", Key="inbound/good.csv", Body=b"partner,amount\nA,1\n")
    h.lambda_handler(s3_event("inbound/good.csv"), None)
    assert boto3.resource("dynamodb").Table("cat").get_item(Key={"pk": "FILE#inbound/good.csv"})["Item"]["status"] == "ACCEPTED"
    s3.put_object(Bucket="land", Key="inbound/poison.csv", Body=b"<html>nope</html>")
    h.lambda_handler(s3_event("inbound/poison.csv"), None)
    assert boto3.resource("dynamodb").Table("cat").get_item(Key={"pk": "FILE#inbound/poison.csv"})["Item"]["status"] == "QUARANTINED"
    s3.put_object(Bucket="land", Key="inbound/dup.csv", Body=b"partner,amount\nA,1\n")
    h.lambda_handler(s3_event("inbound/dup.csv"), None)
    assert boto3.resource("dynamodb").Table("cat").get_item(Key={"pk": "FILE#inbound/dup.csv"})["Item"]["status"] == "DUPLICATE"


@mock_aws
def test_lab15_hitl_does_not_write_until_approve():
    os.environ["CATALOG_TABLE"] = "cat"
    os.environ["APPROVAL_TABLE"] = "appr"
    _create_table("cat")
    _create_table("appr")
    boto3.resource("dynamodb").Table("cat").put_item(Item={"pk": "FILE#demo.csv", "status": "QUARANTINED"})
    h = _load("lab15_tools")
    pending = json.loads(
        h.lambda_handler({"rawPath": "/tools", "body": json.dumps({"tool": "RequestReprocess", "fileId": "FILE#demo.csv"})}, None)["body"]
    )
    assert pending["status"] == "PENDING_APPROVAL"
    still = boto3.resource("dynamodb").Table("cat").get_item(Key={"pk": "FILE#demo.csv"})["Item"]["status"]
    assert still == "QUARANTINED"
    done = json.loads(
        h.lambda_handler({"rawPath": "/approve", "body": json.dumps({"approvalId": pending["approvalId"]})}, None)["body"]
    )
    assert done["status"] == "REPROCESSED"
    assert boto3.resource("dynamodb").Table("cat").get_item(Key={"pk": "FILE#demo.csv"})["Item"]["status"] == "REPROCESSED"


@mock_aws
def test_healthcare_authz():
    os.environ["TABLE_NAME"] = "pt"
    _create_table("pt")
    boto3.resource("dynamodb").Table("pt").put_item(Item={"pk": "PT#pt-1", "patientId": "pt-1", "name": "A", "status": "active"})
    h = _load("cap_health_patients")
    forbidden = h.lambda_handler(
        {
            "rawPath": "/patients/pt-1",
            "pathParameters": {"id": "pt-1"},
            "headers": {"x-actor-role": "patient", "x-actor-id": "pt-2"},
        },
        None,
    )
    assert forbidden["statusCode"] == 403
    ok = h.lambda_handler(
        {
            "rawPath": "/patients/pt-1",
            "pathParameters": {"id": "pt-1"},
            "headers": {"x-actor-role": "clinician", "x-actor-id": "clin-1"},
        },
        None,
    )
    assert ok["statusCode"] == 200


@mock_aws
def test_ecommerce_compensation_unit():
    os.environ["TABLE_NAME"] = "orders"
    os.environ["BUS_NAME"] = "bus"
    _create_table("orders")
    boto3.client("events", region_name="us-west-2").create_event_bus(Name="bus")
    boto3.resource("dynamodb").Table("orders").put_item(Item={"pk": "ORDER#o1", "orderId": "o1", "status": "ACCEPTED"})
    saga = _load("cap_ecom_saga")
    saga.lambda_handler({"detail-type": "InventoryFailed", "detail": {"orderId": "o1", "correlationId": "c"}}, None)
    item = boto3.resource("dynamodb").Table("orders").get_item(Key={"pk": "ORDER#o1"})["Item"]
    assert item["status"] == "COMPENSATED"
    assert item["paymentStatus"] == "VOIDED"


def test_strangler_demo_script():
    import runpy

    runpy.run_path(str(ROOT / "labs" / "lab-08-esb-modernization" / "strangler_demo.py"), run_name="__main__")
