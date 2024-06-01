Sure, here's a detailed step-by-step guide to setting up AWS Transfer Family for SFTP. This guide will cover creating an SFTP server, configuring IAM roles and policies, setting up user accounts, and testing the setup.

### Prerequisites

- AWS account with necessary permissions.
- Basic knowledge of AWS IAM, S3, and the AWS Management Console.
- Terraform installed and configured (optional if you prefer using the AWS Management Console).

### Step 1: Create an IAM Role and Policy

1. **Create an IAM Role**:
   - Open the IAM console.
   - Click on "Roles" and then "Create role".
   - Choose "AWS Service" and select "Transfer" as the service.
   - Click "Next: Permissions".
   - Skip the permission step as we will add a policy later.
   - Click "Next: Tags" and add tags if needed.
   - Click "Next: Review", give the role a name (e.g., "SFTPTransferRole"), and create the role.

2. **Create an IAM Policy**:
   - Go to the IAM console.
   - Click on "Policies" and then "Create policy".
   - Switch to the "JSON" tab and paste the following policy (replace `my-sftp-bucket` with your bucket name):
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": [
             "s3:ListBucket",
             "s3:GetObject",
             "s3:PutObject"
           ],
           "Resource": [
             "arn:aws:s3:::my-sftp-bucket",
             "arn:aws:s3:::my-sftp-bucket/*"
           ]
         }
       ]
     }
     ```
   - Click "Next: Tags" and add tags if needed.
   - Click "Next: Review", give the policy a name (e.g., "SFTPS3AccessPolicy"), and create the policy.

3. **Attach the Policy to the Role**:
   - Go back to the IAM console.
   - Find the role you created (e.g., "SFTPTransferRole").
   - Click on the role, go to the "Permissions" tab, and click "Attach policies".
   - Find and select the policy you created (e.g., "SFTPS3AccessPolicy") and attach it to the role.

### Step 2: Create an S3 Bucket

1. **Create an S3 Bucket**:
   - Open the S3 console.
   - Click "Create bucket".
   - Enter a bucket name (e.g., "my-sftp-bucket").
   - Select a region and configure other settings as needed.
   - Click "Create bucket".

### Step 3: Create an AWS Transfer Family Server

1. **Create an SFTP Server**:
   - Open the AWS Transfer Family console.
   - Click "Create server".
   - Select "SFTP" as the protocol.
   - Choose a VPC endpoint or a publicly accessible endpoint as needed.
   - Optionally, specify a custom hostname if you have one.
   - Click "Next".

2. **Configure the Server**:
   - Select "Service managed" for the identity provider type.
   - Choose the IAM role you created earlier (e.g., "SFTPTransferRole").
   - Add tags if needed.
   - Click "Next".

3. **Review and Create**:
   - Review the configuration and click "Create server".

### Step 4: Create User Accounts

1. **Generate SSH Key Pair**:
   - Open a terminal and generate an SSH key pair if you don't already have one.
   ```bash
   ssh-keygen -t rsa -b 2048 -f sftp_user_key
   ```
   - This creates two files: `sftp_user_key` (private key) and `sftp_user_key.pub` (public key).

2. **Create a User in AWS Transfer Family**:
   - In the AWS Transfer Family console, navigate to "Users" and click "Add user".
   - Specify the username (e.g., "sftp_user").
   - Choose the SFTP server created earlier.
   - Assign the IAM role created earlier.
   - Set the home directory type to "Logical" and configure the home directory mappings.
   - Add the SSH public key by pasting the contents of `sftp_user_key.pub`.
   - Click "Add".

### Step 5: Connect and Test

1. **Connect to the SFTP Server**:
   - Use an SFTP client (e.g., FileZilla, WinSCP) or command-line tool to connect.
   - Host: `<server-endpoint>`
   - Port: 22
   - Protocol: SFTP
   - Username: `sftp_user`
   - Authentication: Use the private key `sftp_user_key`.

   Example command using `sftp`:
   ```bash
   sftp -i path/to/sftp_user_key sftp_user@<server-endpoint>
   ```

2. **Upload and List Files**:
   - Upload a test file to the SFTP server.
   - List the files in the SFTP server to ensure the file was uploaded successfully.

   Example SFTP session:
   ```bash
   sftp -i path/to/sftp_user_key sftp_user@<server-endpoint>
   sftp> put local-file.txt /local-file.txt
   sftp> ls
   ```

### Automate with Terraform (Optional)

If you prefer to use Terraform to automate the setup, here’s a Terraform script:

```hcl
provider "aws" {
  region = "us-west-2"
}

# IAM Role for AWS Transfer Family
resource "aws_iam_role" "sftp_role" {
  name = "SFTPTransferRole"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "transfer.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# IAM Policy for accessing S3 bucket
resource "aws_iam_role_policy" "sftp_policy" {
  name   = "SFTPS3AccessPolicy"
  role   = aws_iam_role.sftp_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject"
        ],
        Resource = [
          "arn:aws:s3:::my-sftp-bucket",
          "arn:aws:s3:::my-sftp-bucket/*"
        ]
      }
    ]
  })
}

# S3 Bucket
resource "aws_s3_bucket" "sftp_bucket" {
  bucket = "my-sftp-bucket"
}

# AWS Transfer Family Server
resource "aws_transfer_server" "sftp_server" {
  endpoint_type = "PUBLIC"
  identity_provider_type = "SERVICE_MANAGED"
  tags = {
    Name = "MySFTPServer"
  }
}

# SFTP User with SSH Key
resource "aws_transfer_user" "sftp_user" {
  user_name          = "sftp_user"
  server_id          = aws_transfer_server.sftp_server.id
  role               = aws_iam_role.sftp_role.arn
  home_directory_type = "LOGICAL"

  home_directory_mappings {
    entry  = "/"
    target = "/my-sftp-bucket"
  }

  ssh_public_key_body = file("path/to/your/sftp_user_key.pub")  # Provide the path to your SSH public key

  tags = {
    Name = "SFTPUser"
  }
}
```

### Summary

By following this step-by-step guide, you will set up an AWS Transfer Family for SFTP, configure necessary IAM roles and policies, create user accounts, and test the setup to ensure everything is functioning correctly. This setup provides a secure and managed solution for transferring files to and from AWS S3 using SFTP.
