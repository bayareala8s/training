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
    logger.info(f"Processing file: s3://{bucket_name}/{object_key}")

    # Retrieve file metadata
    response = s3.head_object(Bucket=bucket_name, Key=object_key)
    metadata = response.get('Metadata', {})
    
    # Check if file is already processed
    if metadata.get('processed') == 'true':
        logger.info(f"File {object_key} is already processed. Skipping.")
        return
    
    # Process the file (placeholder for actual logic)
    process_file(bucket_name, object_key)
    
    # Update metadata to mark the file as processed
    s3.copy_object(
        Bucket=bucket_name,
        CopySource={'Bucket': bucket_name, 'Key': object_key},
        Key=object_key,
        Metadata={**metadata, 'processed': 'true'},
        MetadataDirective='REPLACE'
    )
    logger.info(f"File {object_key} marked as processed.")

def process_file(bucket, key):
    """
    Placeholder function to process the file.
    Replace this logic with your actual file processing.
    """
    logger.info(f"Processing logic executed for {key} in bucket {bucket}.")
