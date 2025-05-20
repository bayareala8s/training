import json

def lambda_handler(event, context):
    try:
        # Parse input JSON
        onboarding_json = event.get("body")
        if isinstance(onboarding_json, str):
            onboarding_json = json.loads(onboarding_json)

        # Top-level required keys
        required_top_keys = ["customerId", "environment", "workflowId", "source", "destination", "schedule"]
        for key in required_top_keys:
            if key not in onboarding_json:
                return error(f"Missing required top-level key: {key}")

        # Validate environment
        if onboarding_json["environment"] not in ["dev", "test", "prod"]:
            return error("Invalid value for 'environment'. Must be one of: dev, test, prod")

        # Validate source
        source = onboarding_json["source"]
        for key in ["type", "host", "port", "username", "authentication", "path"]:
            if key not in source:
                return error(f"Missing key in 'source': {key}")
        if source["type"] != "SFTP":
            return error("source.type must be 'SFTP'")
        if not isinstance(source["port"], int):
            return error("source.port must be an integer")

        # Validate authentication
        auth = source["authentication"]
        if auth["method"] not in ["ssh_key", "password"]:
            return error("authentication.method must be 'ssh_key' or 'password'")
        if "keyName" not in auth:
            return error("Missing 'keyName' in authentication")

        # Validate destination
        dest = onboarding_json["destination"]
        for key in ["type", "bucket", "prefix"]:
            if key not in dest:
                return error(f"Missing key in 'destination': {key}")
        if dest["type"] != "S3":
            return error("destination.type must be 'S3'")

        # Validate schedule
        schedule = onboarding_json["schedule"]
        if schedule.get("type") != "cron":
            return error("schedule.type must be 'cron'")
        if "expression" not in schedule:
            return error("Missing 'expression' in schedule")

        # If all checks pass
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "✅ JSON is valid.",
                "valid": True
            })
        }

    except Exception as ex:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": f"❌ Unexpected error: {str(ex)}",
                "valid": False
            })
        }


def error(msg):
    return {
        "statusCode": 400,
        "body": json.dumps({
            "message": f"❌ Validation failed: {msg}",
            "valid": False
        })
    }
