"""Lab 4: publish workflow outcome to SNS."""
import json
import os

import boto3

sns = boto3.client("sns")


def handler(event, context):
    topic = os.environ["SNS_TOPIC_ARN"]
    valid = event.get("valid", False)
    subject = "BayLearn MFT workflow success" if valid else "BayLearn MFT workflow failure"
    message = json.dumps(event, default=str)
    sns.publish(TopicArn=topic, Subject=subject[:100], Message=message)
    print(json.dumps({"published": topic, "valid": valid}))
    return event
