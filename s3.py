import boto3
import json
import os

# Initialize boto3 clients for STS (to assume roles) and S3
sts_client = boto3.client('sts')
s3_client = boto3.client('s3')

def assume_role(account_id, role_name):
    """Assume IAM role in target account to get temporary credentials."""
    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="LambdaCrossAccountSession"
    )
    return assumed_role['Credentials']

def get_s3_client(credentials):
    """Create S3 client using temporary credentials."""
    return boto3.client(
        's3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )

def list_s3_files(bucket_name, prefix=""):
    """List files in an S3 bucket with a given prefix."""
    s3_files = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    return [file['Key'] for file in s3_files.get('Contents', [])]

def lambda_handler(event, context):
    # Source and target bucket names
    source_bucket = "source-bucket-name"
    target_bucket = "target-bucket-name"
    
    # Prefixes for file filtering (can be dynamic based on the event or other inputs)
    source_prefix = "source-prefix/"
    target_prefix = "target-prefix/"
    
    # Assume role in target account to access the target S3 bucket
    credentials = assume_role("TARGET_ACCOUNT_ID", "S3AccessRole")
    s3_target_client = get_s3_client(credentials)
    
    # List files in source and target buckets
    source_files = list_s3_files(source_bucket, source_prefix)
    target_files = list_s3_files(target_bucket, target_prefix)
    
    # Compare files between source and target
    discrepancies = []
    
    # Files in source but not in target
    for file in source_files:
        if file not in target_files:
            discrepancies.append(f"File {file} exists in source but not in target.")
    
    # Files in target but not in source
    for file in target_files:
        if file not in source_files:
            discrepancies.append(f"File {file} exists in target but not in source.")
    
    # Return result
    if discrepancies:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Discrepancies found between source and target files.',
                'discrepancies': discrepancies
            })
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Files are identical between source and target.'})
    }
