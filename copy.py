import boto3
import os

SOURCE_REGION = 'us-west-2'
DEST_REGION = 'us-east-1'

def lambda_handler(event, context):
    source_bucket = event['source_bucket']
    source_key = event['source_key']
    dest_bucket = event['dest_bucket']
    dest_key = source_key  # or customize as needed

    # Create clients for source and destination
    s3_source = boto3.client('s3', region_name=SOURCE_REGION)
    s3_dest = boto3.client('s3', region_name=DEST_REGION)

    # Initiate multipart upload in destination bucket
    multipart_upload = s3_dest.create_multipart_upload(Bucket=dest_bucket, Key=dest_key)
    upload_id = multipart_upload['UploadId']

    try:
        # Get object metadata to determine size
        metadata = s3_source.head_object(Bucket=source_bucket, Key=source_key)
        total_size = metadata['ContentLength']
        part_size = 50 * 1024 * 1024  # 50MB per part

        parts = []
        byte_position = 0
        part_number = 1

        while byte_position < total_size:
            end_byte = min(byte_position + part_size - 1, total_size - 1)
            byte_range = f"bytes={byte_position}-{end_byte}"

            # Download part from source
            response = s3_source.get_object(Bucket=source_bucket, Key=source_key, Range=byte_range)
            part_data = response['Body'].read()

            # Upload part to destination
            upload_part = s3_dest.upload_part(
                Bucket=dest_bucket,
                Key=dest_key,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=part_data
            )

            parts.append({'ETag': upload_part['ETag'], 'PartNumber': part_number})
            byte_position += part_size
            part_number += 1

        # Complete multipart upload
        s3_dest.complete_multipart_upload(
            Bucket=dest_bucket,
            Key=dest_key,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )
        return {"status": "success", "file": dest_key}

    except Exception as e:
        # Abort multipart upload if something goes wrong
        s3_dest.abort_multipart_upload(Bucket=dest_bucket, Key=dest_key, UploadId=upload_id)
        raise RuntimeError(f"Copy failed: {str(e)}")
