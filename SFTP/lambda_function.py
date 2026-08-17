import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb")

# Environment variable for the table name (set in Terraform)
import os
TABLE_NAME = os.getenv("TABLE_NAME", "CustomerRegistration")
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Main Lambda function handler for CRUD operations.
    """
    try:
        # Extract operation and payload from the event
        operation = event.get("operation")
        payload = event.get("payload", {})

        # Route to the correct operation
        if operation == "create":
            return create_customer(payload)
        elif operation == "read":
            return read_customer(payload)
        elif operation == "update":
            return update_customer(payload)
        elif operation == "delete":
            return delete_customer(payload)
        elif operation == "list":
            return list_customers()
        else:
            return {"statusCode": 400, "body": json.dumps("Invalid operation")}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(str(e))}


# Create a new customer
def create_customer(payload):
    try:
        table.put_item(Item=payload)
        return {"statusCode": 200, "body": json.dumps("Customer created successfully")}
    except ClientError as e:
        return {"statusCode": 400, "body": json.dumps(e.response['Error']['Message'])}


# Read a specific customer by CustomerID and Email
def read_customer(payload):
    try:
        response = table.get_item(Key={
            "CustomerID": payload["CustomerID"],
            "Email": payload["Email"]
        })
        if "Item" in response:
            return {"statusCode": 200, "body": json.dumps(response["Item"])}
        else:
            return {"statusCode": 404, "body": json.dumps("Customer not found")}
    except ClientError as e:
        return {"statusCode": 400, "body": json.dumps(e.response['Error']['Message'])}


# Update an existing customer
def update_customer(payload):
    try:
        update_expression = "SET "
        expression_values = {}

        for key, value in payload["updates"].items():
            update_expression += f"{key} = :{key}, "
            expression_values[f":{key}"] = value

        update_expression = update_expression.rstrip(", ")

        table.update_item(
            Key={
                "CustomerID": payload["CustomerID"],
                "Email": payload["Email"]
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values
        )
        return {"statusCode": 200, "body": json.dumps("Customer updated successfully")}
    except ClientError as e:
        return {"statusCode": 400, "body": json.dumps(e.response['Error']['Message'])}


# Delete a customer
def delete_customer(payload):
    try:
        table.delete_item(Key={
            "CustomerID": payload["CustomerID"],
            "Email": payload["Email"]
        })
        return {"statusCode": 200, "body": json.dumps("Customer deleted successfully")}
    except ClientError as e:
        return {"statusCode": 400, "body": json.dumps(e.response['Error']['Message'])}


# List all customers
def list_customers():
    try:
        response = table.scan()
        return {"statusCode": 200, "body": json.dumps(response.get("Items", []))}
    except ClientError as e:
        return {"statusCode": 400, "body": json.dumps(e.response['Error']['Message'])}
