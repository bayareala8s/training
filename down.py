import boto3
import math
import os

# Configurable Constants
SOURCE_BUCKET = 'your-source-bucket'
SOURCE_KEY = 'path/to/large-file.zip'
DEST_BUCKET = 'your-destination-bucket'
DEST_KEY = 'copied/path/large-file.zip'

# Cross-region setup
SOURCE_REGION = 'us-west-2'
DEST_REGION = 'us-east-1'

PART_SIZE = 100 * 1024 * 1024  # 100 MB

def lambda_handler(event, context):
    # Create region-specific S3 clients
    source_s3 = boto3.client('s3', region_name=SOURCE_REGION)
    dest_s3 = boto3.client('s3', region_name=DEST_REGION)

    # Get the size of the source file
    head_response = source_s3.head_object(Bucket=SOURCE_BUCKET, Key=SOURCE_KEY)
    total_size = head_response['ContentLength']
    total_parts = math.ceil(total_size / PART_SIZE)
    
    print(f"Total file size: {total_size} bytes, Parts: {total_parts}")

    # Start multipart upload on destination
    multipart_upload = dest_s3.create_multipart_upload(Bucket=DEST_BUCKET, Key=DEST_KEY)
    upload_id = multipart_upload['UploadId']
    parts = []

    try:
        for part_number in range(1, total_parts + 1):
            start = (part_number - 1) * PART_SIZE
            end = min(start + PART_SIZE - 1, total_size - 1)

            print(f"Downloading bytes {start}-{end} from source S3")
            response = source_s3.get_object(
                Bucket=SOURCE_BUCKET,
                Key=SOURCE_KEY,
                Range=f'bytes={start}-{end}'
            )
            data = response['Body'].read()

            print(f"Uploading part {part_number} to destination S3")
            upload_response = dest_s3.upload_part(
                Bucket=DEST_BUCKET,
                Key=DEST_KEY,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=data
            )

            parts.append({
                'PartNumber': part_number,
                'ETag': upload_response['ETag']
            })

        # Complete multipart upload
        dest_s3.complete_multipart_upload(
            Bucket=DEST_BUCKET,
            Key=DEST_KEY,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )

        print(f"✅ Upload complete: s3://{DEST_BUCKET}/{DEST_KEY}")

    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        dest_s3.abort_multipart_upload(
            Bucket=DEST_BUCKET,
            Key=DEST_KEY,
            UploadId=upload_id
        )
        raise e
