Encrypting data at rest in AWS involves using various services and tools to ensure that your data is encrypted when stored. Here’s a step-by-step guide on how to achieve this for different AWS services:

### 1. **Encrypting an S3 Bucket**

#### Using Server-Side Encryption (SSE-S3)

1. **Navigate to the S3 Console:**
   - Open the Amazon S3 console.

2. **Create or Select a Bucket:**
   - Click on “Create bucket” or select an existing bucket.

3. **Configure Default Encryption:**
   - Go to the “Properties” tab of the bucket.
   - Under “Default encryption,” select “Enable.”
   - Choose “Amazon S3 key (SSE-S3).”

#### Using Server-Side Encryption with AWS KMS (SSE-KMS)

1. **Navigate to the S3 Console:**
   - Open the Amazon S3 console.

2. **Create or Select a Bucket:**
   - Click on “Create bucket” or select an existing bucket.

3. **Configure Default Encryption:**
   - Go to the “Properties” tab of the bucket.
   - Under “Default encryption,” select “Enable.”
   - Choose “AWS Key Management Service key (SSE-KMS).”
   - Select an existing KMS key or create a new one.

#### Terraform Script for SSE-KMS

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "example_bucket" {
  bucket = "example-bucket"
}

resource "aws_kms_key" "example_kms" {
  description             = "Example KMS key"
  deletion_window_in_days = 10
  enable_key_rotation     = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "example_bucket_sse" {
  bucket = aws_s3_bucket.example_bucket.bucket

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.example_kms.key_id
      sse_algorithm     = "aws:kms"
    }
  }
}
```

### 2. **Encrypting an EBS Volume**

1. **Navigate to the EC2 Console:**
   - Open the Amazon EC2 console.

2. **Create an EBS Volume:**
   - Select “Volumes” under “Elastic Block Store” in the left navigation pane.
   - Click “Create Volume.”
   - Choose the desired volume type and size.
   - Under “Encryption,” select the “Encrypt this volume” checkbox.
   - Select an existing KMS key or use the default key.

3. **Attach the EBS Volume to an EC2 Instance:**
   - Select the volume, then click “Actions” > “Attach Volume.”
   - Choose the instance to attach the volume to and click “Attach.”

#### Terraform Script for Encrypted EBS Volume

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_kms_key" "example_kms" {
  description             = "Example KMS key"
  deletion_window_in_days = 10
  enable_key_rotation     = true
}

resource "aws_ebs_volume" "example_volume" {
  availability_zone = "us-west-2a"
  size              = 10
  encrypted         = true
  kms_key_id        = aws_kms_key.example_kms.arn
}

resource "aws_instance" "example_instance" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t2.micro"

  ebs_block_device {
    device_name = "/dev/sdh"
    volume_id   = aws_ebs_volume.example_volume.id
  }
}
```

### 3. **Encrypting an RDS Instance**

1. **Navigate to the RDS Console:**
   - Open the Amazon RDS console.

2. **Create an RDS Instance:**
   - Click on “Create database.”
   - Choose a database creation method and engine.
   - Under “Settings,” choose “Enable encryption.”
   - Select an existing KMS key or use the default key.

#### Terraform Script for Encrypted RDS Instance

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_kms_key" "example_kms" {
  description             = "Example KMS key"
  deletion_window_in_days = 10
  enable_key_rotation     = true
}

resource "aws_db_instance" "example_rds" {
  allocated_storage    = 20
  engine               = "mysql"
  instance_class       = "db.t3.micro"
  name                 = "exampledb"
  username             = "admin"
  password             = "password"
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot  = true

  storage_encrypted = true
  kms_key_id        = aws_kms_key.example_kms.key_id
}
```

### 4. **Encrypting Data in DynamoDB**

1. **Navigate to the DynamoDB Console:**
   - Open the Amazon DynamoDB console.

2. **Create a DynamoDB Table:**
   - Click on “Create table.”
   - Specify the table name and primary key.
   - Under “Encryption,” choose “AWS owned key” (default) or “AWS managed key” or “Customer managed key” for more control.

#### Terraform Script for Encrypted DynamoDB Table

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_kms_key" "example_kms" {
  description             = "Example KMS key"
  deletion_window_in_days = 10
  enable_key_rotation     = true
}

resource "aws_dynamodb_table" "example_table" {
  name           = "example-table"
  hash_key       = "id"
  billing_mode   = "PAY_PER_REQUEST"
  kms_key_arn    = aws_kms_key.example_kms.arn

  attribute {
    name = "id"
    type = "S"
  }
}
```

### Best Practices for Encrypting Data at Rest

1. **Use KMS for Key Management:**
   - AWS KMS provides centralized key management with fine-grained access controls.

2. **Enable Encryption by Default:**
   - Configure services to encrypt data by default.

3. **Regularly Rotate Keys:**
   - Enable key rotation to automatically rotate keys annually.

4. **Monitor and Audit Key Usage:**
   - Use AWS CloudTrail to monitor and audit key usage.

5. **Ensure Secure Key Storage:**
   - Store keys securely and restrict access to authorized users only.

By following these steps and using the provided Terraform scripts, you can ensure that your data at rest is securely encrypted across various AWS services.
