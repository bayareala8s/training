import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('processed-data')

def handler(event, context):
    # Process the file
    for record in event['Records']:
        s3 = record['s3']
        bucket = s3['bucket']['name']
        key = s3['object']['key']
        
        # Mock processing logic
        processed_data = {
            'file_id': key,
            'content': 'processed content'
        }
        
        # Store in DynamoDB
        table.put_item(Item=processed_data)
    
    return {
        'statusCode': 200,
        'body': json.dumps('File processed successfully')
    }
