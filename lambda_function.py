import boto3
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        config = json.loads(os.environ['CONFIG'])
        source_bucket = config['source_bucket']
        target_bucket = config['target_bucket']

        for record in event['Records']:
            source_key = record['s3']['object']['key']

            # Copy the file
            copy_source = {'Bucket': source_bucket, 'Key': source_key}
            s3_client.copy_object(Bucket=target_bucket, Key=source_key, CopySource=copy_source)

            logger.info(f"Successfully copied {source_key} from {source_bucket} to {target_bucket}")

    except Exception as e:
        logger.error(f"Error copying file: {e}")
        raise
