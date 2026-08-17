import boto3
import paramiko
import os
import json

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

def get_sftp_client(server_id):
    """Connect to the correct SFTP server using credentials stored in environment variables."""
    if server_id == "server1":
        host = os.environ['SFTP_HOST_1']
        username = os.environ['SFTP_USERNAME_1']
        password = os.environ['SFTP_PASSWORD_1']
    elif server_id == "server2":
        host = os.environ['SFTP_HOST_2']
        username = os.environ['SFTP_USERNAME_2']
        password = os.environ['SFTP_PASSWORD_2']
    else:
        raise ValueError("Invalid server_id")

    # Establish the SFTP connection
    transport = paramiko.Transport((host, 22))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp

def lambda_handler(event, context):
    # SFTP and S3 bucket details
    source_sftp_server = "server1"
    target_s3_bucket = "target-bucket-name"
    sftp_prefix = "sftp-prefix/"
    s3_prefix = "s3-prefix/"
    
    # Assume role in the target account to access the target S3 bucket
    credentials = assume_role("TARGET_ACCOUNT_ID", "S3AccessRole")
    s3_target_client = get_s3_client(credentials)
    
    # List files from the SFTP server
    sftp_client = get_sftp_client(source_sftp_server)
    sftp_files = sftp_client.listdir_attr(sftp_prefix)  # List files in SFTP directory with prefix
    sftp_file_names = [file.filename for file in sftp_files]

    # List files from the target S3 bucket
    s3_files = list_s3_files(target_s3_bucket, s3_prefix)
    
    # Compare files between SFTP and S3
    discrepancies = []

    # Files in SFTP but not in S3
    for file in sftp_file_names:
        if file not in s3_files:
            discrepancies.append(f"File {file} exists in SFTP but not in S3.")
    
    # Files in S3 but not in SFTP
    for file in s3_files:
        if file not in sftp_file_names:
            discrepancies.append(f"File {file} exists in S3 but not in SFTP.")
    
    # Return result
    if discrepancies:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Discrepancies found between SFTP and S3 files.',
                'discrepancies': discrepancies
            })
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Files are identical between SFTP and S3.'})
    }
