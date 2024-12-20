import boto3
import logging

# Initialize S3 client
s3 = boto3.client('s3')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def lambda_handler(event, context):
    # Parse S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    logger.info(f"Replicated file detected: s3://{bucket_name}/{object_key}")

    # Retrieve file metadata
    response = s3.head_object(Bucket=bucket_name, Key=object_key)
    metadata = response.get('Metadata', {})
    
    # Check if file is already processed
    if metadata.get('processed') == 'true':
        logger.info(f"File {object_key} is already processed in replica bucket. Skipping.")
        return
    
    # Process the file (placeholder for actual logic)
    process_file(bucket_name, object_key)
    logger.info(f"File {object_key} processed by backup Lambda.")

def process_file(bucket, key):
    """
    Placeholder function to process the file.
    Replace this logic with your actual file processing.
    """
    logger.info(f"Processing logic executed for {key} in bucket {bucket}.")
