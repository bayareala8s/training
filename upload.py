import boto3
import os

SOURCE_BUCKET = 'your-source-bucket'
SOURCE_KEY = 'path/to/large-file.zip'
DEST_BUCKET = 'your-dest-bucket'
DEST_KEY = 'path/to/large-file.zip'
PART_SIZE = 100 * 1024 * 1024  # 100 MB

def lambda_handler(event, context):
    # Source session (us-west-2)
    source_s3 = boto3.client('s3', region_name='us-west-2')

    # Destination session (us-east-1)
    dest_s3 = boto3.client('s3', region_name='us-east-1')

    # Get file size
    head = source_s3.head_object(Bucket=SOURCE_BUCKET, Key=SOURCE_KEY)
    total_size = head['ContentLength']

    # Initiate multipart upload on destination
    multipart_upload = dest_s3.create_multipart_upload(Bucket=DEST_BUCKET, Key=DEST_KEY)
    upload_id = multipart_upload['UploadId']
    parts = []

    try:
        part_number = 1
        byte_position = 0

        while byte_position < total_size:
            last_byte = min(byte_position + PART_SIZE - 1, total_size - 1)

            # Download part from source
            response = source_s3.get_object(
                Bucket=SOURCE_BUCKET,
                Key=SOURCE_KEY,
                Range=f'bytes={byte_position}-{last_byte}'
            )
            body = response['Body'].read()

            # Upload part to destination
            upload_part = dest_s3.upload_part(
                Bucket=DEST_BUCKET,
                Key=DEST_KEY,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=body
            )

            parts.append({
                'PartNumber': part_number,
                'ETag': upload_part['ETag']
            })

            print(f'Uploaded part {part_number}, bytes {byte_position}-{last_byte}')
            part_number += 1
            byte_position += PART_SIZE

        # Complete the upload
        dest_s3.complete_multipart_upload(
            Bucket=DEST_BUCKET,
            Key=DEST_KEY,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )
        print('Upload completed successfully.')

    except Exception as e:
        print(f'Error: {str(e)}')
        dest_s3.abort_multipart_upload(Bucket=DEST_BUCKET, Key=DEST_KEY, UploadId=upload_id)
        raise
