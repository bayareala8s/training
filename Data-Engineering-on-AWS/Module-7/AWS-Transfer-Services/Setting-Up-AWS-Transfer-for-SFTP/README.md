Here's a detailed step-by-step guide to setting up AWS Transfer Family for SFTP. This guide will cover creating an SFTP server, configuring IAM roles and policies, setting up user accounts, and testing the setup.

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



To transfer large files (like 100GB) using AWS Transfer Family (AWS Transfer for SFTP, FTPS, and FTP), follow these steps:

1. **Set Up an AWS Transfer Family Server**:
   - Go to the AWS Transfer Family console.
   - Click on "Create server."
   - Choose the protocol you want to use (SFTP, FTPS, or FTP).
   - Configure endpoint settings: choose either "Publicly accessible" or "VPC."
   - Set up identity provider: choose how you want to manage user access (Service-managed, Custom, or AWS Directory Service).
   - Add tags if needed.
   - Click "Create server."

2. **Create a User**:
   - After creating the server, go to "Users" and click "Add user."
   - Specify the username.
   - Select the Identity provider type (Service-managed, Custom, or AWS Directory Service).
   - For Service-managed, create an IAM role with permissions to the S3 bucket where the files will be transferred.
   - Specify the home directory for the user in the S3 bucket.
   - Configure the SSH public key for SFTP or set up password authentication for FTP/FTPS.
   - Click "Add."

3. **Configure the Client**:
   - Use an SFTP, FTPS, or FTP client to connect to the AWS Transfer Family server.
   - For SFTP: Use the user credentials (username and SSH key) to connect.
   - For FTPS/FTP: Use the user credentials (username and password).

4. **Transfer the Files**:
   - Open your SFTP/FTPS/FTP client (such as FileZilla, WinSCP, or Cyberduck).
   - Connect to the AWS Transfer Family server using the configured user credentials.
   - Navigate to the source directory on your local machine.
   - Select the files or directories you want to transfer.
   - Drag and drop the files or directories to the destination S3 bucket in the client interface.
   - Monitor the transfer to ensure it completes successfully.

### Example using AWS CLI and SFTP

1. **Create the Server (AWS Transfer Family)**:
```bash
aws transfer create-server --protocols SFTP --endpoint-type PUBLIC
```

2. **Create an IAM Role for the Transfer User**:
   - Create a policy with S3 permissions.
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
        "arn:aws:s3:::your-bucket-name",
        "arn:aws:s3:::your-bucket-name/*"
      ]
    }
  ]
}
```
   - Create the role and attach the policy.

3. **Create the User**:
```bash
aws transfer create-user --server-id server-id --user-name username --role arn:aws:iam::account-id:role/role-name --home-directory "/your-bucket-name" --ssh-public-key file://path/to/ssh-public-key
```

4. **Transfer Files Using SFTP Client**:
   - Connect to the server using the SFTP client with the username and SSH key.
   - Upload files to the S3 bucket directory.

### Tips for Large File Transfers

- **Parallel Transfers**: Use multiple parallel connections to speed up the transfer.
- **Network Speed**: Ensure you have a good network connection to avoid interruptions.
- **Check File Integrity**: Verify file integrity after transfer using checksums.

By following these steps, you can efficiently transfer large files to AWS using Transfer Family services.


Using multiple parallel connections can significantly speed up the transfer of large files with AWS Transfer Family. Here's a detailed guide on how to set up parallel transfers:

### 1. **Set Up AWS Transfer Family**

Ensure you have already set up an AWS Transfer Family server and created a user with appropriate permissions as described in the previous steps.

### 2. **Choose an SFTP Client that Supports Parallel Transfers**

Not all SFTP clients support parallel transfers. Some popular clients that do include:
- **FileZilla**
- **WinSCP**
- **Cyberduck**

### 3. **Configure Parallel Transfers in Your SFTP Client**

#### **FileZilla**

1. **Install and Open FileZilla**:
   - Download and install FileZilla from the [official website](https://filezilla-project.org/).

2. **Connect to Your AWS Transfer Family Server**:
   - Open FileZilla.
   - Go to `File > Site Manager`.
   - Click `New Site` and fill in the details:
     - Host: Your AWS Transfer Family server endpoint.
     - Protocol: SFTP - SSH File Transfer Protocol.
     - Logon Type: Normal.
     - User: Your SFTP username.
     - Key file: Browse and select your SSH private key file.

3. **Set Up Parallel Transfers**:
   - Go to `Edit > Settings`.
   - Under `Transfers`, adjust the following settings:
     - `Maximum simultaneous transfers`: Set this to a higher number, such as 10 or 20.
     - `Limit for concurrent downloads/uploads`: Ensure these values are high enough to utilize multiple connections.

4. **Start the Transfer**:
   - Connect to the server using the settings saved in Site Manager.
   - Drag and drop your files or directories into the queue.
   - FileZilla will handle multiple parallel transfers according to your settings.

#### **WinSCP**

1. **Install and Open WinSCP**:
   - Download and install WinSCP from the [official website](https://winscp.net/eng/index.php).

2. **Connect to Your AWS Transfer Family Server**:
   - Open WinSCP.
   - Click `New Site` and fill in the details:
     - File protocol: SFTP.
     - Host name: Your AWS Transfer Family server endpoint.
     - User name: Your SFTP username.
     - Private key file: Browse and select your SSH private key file.

3. **Set Up Parallel Transfers**:
   - Before connecting, click `Advanced`.
   - Under `Environment`, go to `SFTP`.
   - Set `Number of allowed concurrent file transfers` to a higher number (e.g., 10 or 20).

4. **Start the Transfer**:
   - Connect using the saved session.
   - Transfer your files using drag and drop or other file management options within WinSCP.

#### **Cyberduck**

1. **Install and Open Cyberduck**:
   - Download and install Cyberduck from the [official website](https://cyberduck.io/).

2. **Connect to Your AWS Transfer Family Server**:
   - Open Cyberduck.
   - Click the `Open Connection` button.
   - Fill in the details:
     - Server: Your AWS Transfer Family server endpoint.
     - Username: Your SFTP username.
     - Choose `SFTP (SSH File Transfer Protocol)` as the connection type.
     - Use your SSH private key for authentication.

3. **Set Up Parallel Transfers**:
   - Cyberduck handles transfers slightly differently and does not have a specific setting for parallel transfers like FileZilla or WinSCP. However, it can handle multiple uploads/downloads simultaneously from its Transfer window.

4. **Start the Transfer**:
   - Connect to the server.
   - Drag and drop files to the remote directory.
   - Multiple files will be transferred simultaneously by default.

### Tips for Efficient Parallel Transfers

- **File Splitting**: For extremely large files, consider splitting them into smaller parts before transfer and reassembling them after the transfer. Tools like `split` and `cat` in Unix or third-party software in Windows can help with this.
- **Monitoring**: Monitor the transfer to ensure no connections are dropped. If any issues arise, you can retry failed transfers.
- **Network Optimization**: Ensure your network connection is stable and optimized for high-speed transfers.

By configuring your SFTP client for parallel transfers, you can significantly reduce the time required to transfer large files using AWS Transfer Family.
