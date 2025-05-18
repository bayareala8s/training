import json
import boto3
import datetime

# S3 bucket to store JSON output
S3_BUCKET_NAME = "your-json-storage-bucket"

def lambda_handler(event, context):
    try:
        # Extract slots from Lex V2 event
        slots = event['sessionState']['intent']['slots']

        # Extract slot values safely
        def get_slot(slot_name):
            return slots.get(slot_name, {}).get('value', {}).get('interpretedValue', '')

        # Construct the JSON object
        json_payload = {
            "customerId": get_slot("customerId"),
            "environment": get_slot("environment"),
            "workflowId": get_slot("workflowId"),
            "source": {
                "type": get_slot("sourceType"),
                "host": get_slot("sourceHost"),
                "port": int(get_slot("sourcePort")),
                "username": get_slot("sourceUsername"),
                "authentication": {
                    "method": get_slot("authMethod"),
                    "keyName": get_slot("authKey")
                },
                "path": get_slot("sourcePath")
            },
            "destination": {
                "type": "S3",
                "bucket": get_slot("destBucket"),
                "prefix": get_slot("destPrefix")
            },
            "schedule": {
                "type": "cron",
                "expression": get_slot("cronSchedule")
            }
        }

        # Generate a unique filename for the customer JSON
        filename = f"{json_payload['customerId']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # Upload the JSON to S3
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=filename,
            Body=json.dumps(json_payload, indent=2),
            ContentType='application/json'
        )

        # Prepare Lex response
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": event['sessionState']['intent']['name'],
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": f"✅ Customer onboarding JSON created and stored in S3 as `{filename}`"
                }
            ]
        }

    except Exception as e:
        print("Error:", e)
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": event['sessionState']['intent']['name'],
                    "state": "Failed"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": f"❌ Error occurred while generating onboarding JSON: {str(e)}"
                }
            ]
        }
