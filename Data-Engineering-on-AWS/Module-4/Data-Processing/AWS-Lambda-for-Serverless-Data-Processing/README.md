# Detailed Guide for AWS Lambda for Serverless Data Processing

## Overview
AWS Lambda is a serverless compute service that lets you run code without provisioning or managing servers. It is perfect for data processing tasks where you need to handle data at scale, process real-time streams, or perform event-driven tasks.

This guide will cover the following topics:
1. Introduction to AWS Lambda
2. Setting Up Your AWS Environment
3. Creating Your First Lambda Function
4. Integrating AWS Lambda with Other AWS Services
5. Best Practices for AWS Lambda
6. Real-world Use Cases and Examples

## 1. Introduction to AWS Lambda

### What is AWS Lambda?
- Serverless compute service
- Automatic scaling
- Pay only for compute time used

### Key Features
- Event-driven
- Automatic scaling
- Supports multiple programming languages (Node.js, Python, Ruby, Java, Go, .NET, etc.)

### Use Cases
- Real-time file processing
- Data transformation and ETL
- Backend for mobile applications
- Real-time stream processing

## 2. Setting Up Your AWS Environment

### Prerequisites
- AWS Account
- IAM User with appropriate permissions

### AWS CLI Installation
1. Download and install the AWS CLI from the [official AWS CLI page](https://aws.amazon.com/cli/).
2. Configure the AWS CLI with your credentials:
   ```bash
   aws configure
   ```

### Setting Up IAM Role for Lambda
1. Go to the IAM console.
2. Create a new role with the following policies:
   - AWSLambdaBasicExecutionRole
   - Additional policies as per your use case (e.g., S3 access, DynamoDB access)

## 3. Creating Your First Lambda Function

### Using the AWS Management Console
1. Navigate to the AWS Lambda console.
2. Click on "Create function".
3. Choose "Author from scratch".
4. Configure the following settings:
   - Function name: MyFirstLambda
   - Runtime: Python 3.x (or any other supported runtime)
   - Role: Choose the IAM role created earlier
5. Click on "Create function".

### Writing Your Lambda Function
1. In the function code editor, write a simple Lambda function:
   ```python
   import json

   def lambda_handler(event, context):
       return {
           'statusCode': 200,
           'body': json.dumps('Hello from Lambda!')
       }
   ```
2. Click on "Deploy".

### Testing Your Lambda Function
1. Click on "Test".
2. Configure a test event and click "Create".
3. Click "Test" again to execute the function.

## 4. Integrating AWS Lambda with Other AWS Services

### S3 Trigger
1. Go to the S3 console.
2. Choose a bucket and configure an event notification.
3. Set the event type (e.g., ObjectCreated) and select the Lambda function.

### DynamoDB Trigger
1. Go to the DynamoDB console.
2. Choose a table and configure a trigger.
3. Select the Lambda function.

### API Gateway Integration
1. Go to the API Gateway console.
2. Create a new API.
3. Create a resource and a method.
4. Integrate the method with the Lambda function.

### Kinesis Stream Trigger
1. Go to the Kinesis console.
2. Create a data stream.
3. Configure the stream to trigger the Lambda function.

## 5. Best Practices for AWS Lambda

### Performance Optimization
- Use environment variables for configuration.
- Minimize deployment package size.
- Avoid long-running processes.

### Cost Optimization
- Monitor usage with AWS CloudWatch.
- Optimize function memory allocation.
- Use Provisioned Concurrency for consistent start times.

### Security
- Use IAM roles with the least privilege.
- Encrypt sensitive data using AWS KMS.
- Implement logging and monitoring.

### Monitoring and Logging
- Use AWS CloudWatch for monitoring.
- Implement custom metrics and alarms.
- Enable AWS X-Ray for tracing.

## 6. Real-world Use Cases and Examples

### Real-time File Processing
1. Upload files to an S3 bucket.
2. Trigger a Lambda function to process the files.
3. Store processed data in a DynamoDB table.

### Data Transformation and ETL
1. Use AWS Glue to extract data from various sources.
2. Transform data using Lambda functions.
3. Load transformed data into a data warehouse (e.g., Amazon Redshift).

### Real-time Stream Processing
1. Stream data into an Amazon Kinesis stream.
2. Trigger Lambda functions to process each record.
3. Store the processed data in an S3 bucket or a DynamoDB table.

### Backend for Mobile Applications
1. Use Amazon API Gateway to expose APIs.
2. Implement business logic in Lambda functions.
3. Store and retrieve data from DynamoDB.

By following this guide, you will be able to harness the power of AWS Lambda for serverless data processing and build scalable, efficient, and cost-effective solutions.


# Step-by-Step Guide for Real-time File Processing with AWS Lambda

This guide will walk you through setting up a real-time file processing pipeline using AWS Lambda. We will cover the following steps:

1. **Creating an S3 Bucket**
2. **Setting Up IAM Role for Lambda**
3. **Creating a Lambda Function**
4. **Configuring S3 Event Notification**
5. **Testing the Setup**

## 1. Creating an S3 Bucket

### Step 1: Create an S3 Bucket
1. Log in to the AWS Management Console.
2. Navigate to the S3 service.
3. Click on "Create bucket".
4. Enter a unique bucket name (e.g., `my-real-time-file-processing-bucket`).
5. Choose the region and configure other settings as needed.
6. Click on "Create bucket".

## 2. Setting Up IAM Role for Lambda

### Step 2: Create an IAM Role
1. Go to the IAM console.
2. Click on "Roles" in the left sidebar.
3. Click on "Create role".
4. Choose "AWS service" and select "Lambda".
5. Click on "Next: Permissions".
6. Attach the following policies:
   - `AWSLambdaBasicExecutionRole`
   - `AmazonS3ReadOnlyAccess`
7. Click on "Next: Tags", then "Next: Review".
8. Enter a role name (e.g., `LambdaS3AccessRole`).
9. Click on "Create role".

## 3. Creating a Lambda Function

### Step 3: Create a Lambda Function
1. Navigate to the AWS Lambda console.
2. Click on "Create function".
3. Choose "Author from scratch".
4. Configure the following settings:
   - Function name: `RealTimeFileProcessor`
   - Runtime: Python 3.x (or any other supported runtime)
   - Role: Choose the IAM role created earlier (`LambdaS3AccessRole`)
5. Click on "Create function".

### Step 4: Write the Lambda Function Code
1. In the function code editor, write the following code:
   ```python
   import json
   import boto3

   s3 = boto3.client('s3')

   def lambda_handler(event, context):
       # Get the bucket name and file key from the event
       bucket = event['Records'][0]['s3']['bucket']['name']
       key = event['Records'][0]['s3']['object']['key']

       # Fetch the file from S3
       response = s3.get_object(Bucket=bucket, Key=key)
       file_content = response['Body'].read().decode('utf-8')

       # Process the file (for demonstration, we'll just print its content)
       print(f"Processing file from bucket: {bucket}, key: {key}")
       print(f"File content: {file_content}")

       # You can add more processing logic here

       return {
           'statusCode': 200,
           'body': json.dumps('File processed successfully')
       }
   ```
2. Click on "Deploy".

## 4. Configuring S3 Event Notification

### Step 5: Set Up S3 Event Notification
1. Go to the S3 console and navigate to your bucket (`my-real-time-file-processing-bucket`).
2. Click on the "Properties" tab.
3. Scroll down to the "Event notifications" section and click on "Create event notification".
4. Enter a name for the notification (e.g., `FileUploadNotification`).
5. Configure the following settings:
   - Event types: Select "All object create events".
   - Destination: Choose "Lambda function" and select `RealTimeFileProcessor`.
6. Click on "Save changes".

## 5. Testing the Setup

### Step 6: Upload a Test File to S3
1. Navigate to the S3 console and go to your bucket (`my-real-time-file-processing-bucket`).
2. Click on "Upload".
3. Choose a test file from your local system.
4. Click on "Upload".

### Step 7: Verify Lambda Execution
1. Go to the AWS Lambda console.
2. Select your Lambda function (`RealTimeFileProcessor`).
3. Click on the "Monitor" tab and then "View logs in CloudWatch".
4. Check the CloudWatch logs to see the output of your Lambda function. You should see logs indicating that the file was processed successfully and its content was printed.

## Summary

By following these steps, you have set up a real-time file processing pipeline using AWS Lambda and S3. Whenever a new file is uploaded to the S3 bucket, the Lambda function is triggered to process the file. This setup can be extended to include more complex processing logic as per your requirements.


Here's a complete Terraform script to set up the real-time file processing with AWS Lambda and S3 as described in the guide. The script includes creating an S3 bucket, an IAM role, and a Lambda function.

### Step 1: Create the Terraform Configuration File

Create a file named `main.tf` and add the following content:

```hcl
provider "aws" {
  region = "us-east-1"  # Change to your preferred region
}

resource "aws_s3_bucket" "bucket" {
  bucket = "my-real-time-file-processing-bucket"
  acl    = "private"
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Effect    = "Allow"
      Sid       = ""
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "s3_read_access" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

resource "aws_lambda_function" "file_processor" {
  function_name = "RealTimeFileProcessor"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  
  filename = "lambda.zip"

  source_code_hash = filebase64sha256("lambda.zip")
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.file_processor.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.file_processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.bucket.arn
}

output "s3_bucket_name" {
  value = aws_s3_bucket.bucket.bucket
}

output "lambda_function_name" {
  value = aws_lambda_function.file_processor.function_name
}
```

### Step 2: Create the Lambda Function Code

Create a file named `lambda_function.py` with the following content:

```python
import json
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the bucket name and file key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Fetch the file from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    file_content = response['Body'].read().decode('utf-8')

    # Process the file (for demonstration, we'll just print its content)
    print(f"Processing file from bucket: {bucket}, key: {key}")
    print(f"File content: {file_content}")

    # You can add more processing logic here

    return {
        'statusCode': 200,
        'body': json.dumps('File processed successfully')
    }
```

### Step 3: Create a Deployment Package

Zip the `lambda_function.py` file into a deployment package:

```bash
zip lambda.zip lambda_function.py
```

### Step 4: Initialize and Apply the Terraform Configuration

1. Initialize the Terraform configuration:

    ```bash
    terraform init
    ```

2. Apply the Terraform configuration:

    ```bash
    terraform apply
    ```

   Type `yes` when prompted to confirm the creation of resources.

### Summary

By following these steps, you have used Terraform to set up an AWS environment for real-time file processing with AWS Lambda and S3. The Terraform script handles the creation of the S3 bucket, IAM role, Lambda function, and necessary permissions and notifications. Whenever a new file is uploaded to the S3 bucket, the Lambda function will be triggered to process the file.


# Step-by-Step Guide for Data Transformation and ETL with AWS Lambda, S3, and Glue

This guide will walk you through setting up a data transformation and ETL pipeline using AWS Lambda, S3, and AWS Glue. We will cover the following steps:

1. **Setting Up the Environment**
2. **Creating an S3 Bucket**
3. **Setting Up IAM Roles**
4. **Creating and Deploying a Lambda Function**
5. **Configuring S3 Event Notification**
6. **Creating and Running a Glue Job**
7. **Testing the Setup**

## 1. Setting Up the Environment

### Prerequisites
- AWS Account
- AWS CLI installed and configured
- Terraform installed

## 2. Creating an S3 Bucket

### Step 1: Create an S3 Bucket
1. Log in to the AWS Management Console.
2. Navigate to the S3 service.
3. Click on "Create bucket".
4. Enter a unique bucket name (e.g., `my-etl-source-bucket` for source data and `my-etl-target-bucket` for transformed data).
5. Choose the region and configure other settings as needed.
6. Click on "Create bucket".

## 3. Setting Up IAM Roles

### Step 2: Create IAM Roles
1. Go to the IAM console.
2. Click on "Roles" in the left sidebar.
3. Click on "Create role".
4. Choose "AWS service" and select "Lambda".
5. Click on "Next: Permissions".
6. Attach the following policies:
   - `AWSLambdaBasicExecutionRole`
   - `AmazonS3FullAccess`
   - `AWSGlueServiceRole`
7. Click on "Next: Tags", then "Next: Review".
8. Enter a role name (e.g., `LambdaGlueS3AccessRole`).
9. Click on "Create role".

## 4. Creating and Deploying a Lambda Function

### Step 3: Create a Lambda Function
1. Navigate to the AWS Lambda console.
2. Click on "Create function".
3. Choose "Author from scratch".
4. Configure the following settings:
   - Function name: `ETLTriggerLambda`
   - Runtime: Python 3.x (or any other supported runtime)
   - Role: Choose the IAM role created earlier (`LambdaGlueS3AccessRole`)
5. Click on "Create function".

### Step 4: Write the Lambda Function Code
Create a file named `etl_trigger_lambda.py` with the following content:

```python
import json
import boto3

glue = boto3.client('glue')

def lambda_handler(event, context):
    # Start Glue Job
    response = glue.start_job_run(
        JobName='my-glue-job'  # Replace with your Glue job name
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Glue job started')
    }
```

### Step 5: Create a Deployment Package
Zip the `etl_trigger_lambda.py` file into a deployment package:

```bash
zip etl_trigger_lambda.zip etl_trigger_lambda.py
```

### Step 6: Deploy the Lambda Function
1. Upload the deployment package to the Lambda function.
2. Click on "Deploy".

## 5. Configuring S3 Event Notification

### Step 7: Set Up S3 Event Notification
1. Go to the S3 console and navigate to your source bucket (`my-etl-source-bucket`).
2. Click on the "Properties" tab.
3. Scroll down to the "Event notifications" section and click on "Create event notification".
4. Enter a name for the notification (e.g., `FileUploadNotification`).
5. Configure the following settings:
   - Event types: Select "All object create events".
   - Destination: Choose "Lambda function" and select `ETLTriggerLambda`.
6. Click on "Save changes".

## 6. Creating and Running a Glue Job

### Step 8: Create a Glue Crawler
1. Navigate to the AWS Glue console.
2. Click on "Crawlers" in the left sidebar and then "Add crawler".
3. Configure the crawler to scan your source S3 bucket (`my-etl-source-bucket`).
4. Define a new database for the crawler results.
5. Run the crawler to populate the Glue Data Catalog.

### Step 9: Create a Glue Job
1. Navigate to the AWS Glue console.
2. Click on "Jobs" in the left sidebar and then "Add job".
3. Configure the job with the following settings:
   - Name: `my-glue-job`
   - IAM Role: Choose the IAM role created earlier (`LambdaGlueS3AccessRole`)
   - Type: Spark
4. In the script editor, write a transformation script. For example, `etl_script.py`:

```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Define the source
source_df = glueContext.create_dynamic_frame.from_catalog(
    database="my-database",
    table_name="my-table"
)

# Transform data (Example: select specific columns)
transformed_df = source_df.select_fields(['column1', 'column2'])

# Define the target
target_path = "s3://my-etl-target-bucket/transformed-data/"

# Write the transformed data to the target
glueContext.write_dynamic_frame.from_options(
    frame=transformed_df,
    connection_type="s3",
    connection_options={"path": target_path},
    format="json"
)

job.commit()
```

4. Save and run the Glue job.

## 7. Testing the Setup

### Step 10: Upload a Test File to S3
1. Navigate to the S3 console and go to your source bucket (`my-etl-source-bucket`).
2. Click on "Upload".
3. Choose a test file from your local system.
4. Click on "Upload".

### Step 11: Verify Lambda and Glue Execution
1. Go to the AWS Lambda console.
2. Select your Lambda function (`ETLTriggerLambda`).
3. Click on the "Monitor" tab and then "View logs in CloudWatch".
4. Check the CloudWatch logs to see the output of your Lambda function.

### Step 12: Verify Transformed Data in Target S3 Bucket
1. Navigate to the S3 console and go to your target bucket (`my-etl-target-bucket`).
2. Verify that the transformed data is present in the specified location.

## Terraform Script

### Step 13: Create the Terraform Configuration File

Create a file named `main.tf` and add the following content:

```hcl
provider "aws" {
  region = "us-east-1"  # Change to your preferred region
}

resource "aws_s3_bucket" "source_bucket" {
  bucket = "my-etl-source-bucket"
  acl    = "private"
}

resource "aws_s3_bucket" "target_bucket" {
  bucket = "my-etl-target-bucket"
  acl    = "private"
}

resource "aws_iam_role" "lambda_glue_s3_role" {
  name = "lambda_glue_s3_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Effect    = "Allow"
      Sid       = ""
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_glue_s3_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "s3_full_access" {
  role       = aws_iam_role.lambda_glue_s3_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "glue_service_role" {
  role       = aws_iam_role.lambda_glue_s3_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_lambda_function" "etl_trigger_lambda" {
  function_name = "ETLTriggerLambda"
  role          = aws_iam_role.lambda_glue_s3_role.arn
  handler       = "etl_trigger_lambda.lambda_handler"
  runtime       = "python3.8"
  
  filename = "etl_trigger_lambda.zip"

  source_code_hash = filebase64sha256("etl_trigger_lambda.zip")
}

resource "aws_s3_bucket_notification" "source_bucket_notification" {
  bucket = aws_s3_bucket.source_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.etl_trigger_lambda.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.etl_trigger_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.source_bucket.arn
}

output "source_s3_bucket_name" {
 

 value = aws_s3_bucket.source_bucket.bucket
}

output "target_s3_bucket_name" {
  value = aws_s3_bucket.target_bucket.bucket
}

output "lambda_function_name" {
  value = aws_lambda_function.etl_trigger_lambda.function_name
}
```

### Summary

By following these steps, you have set up a data transformation and ETL pipeline using AWS Lambda, S3, and AWS Glue. The Terraform script handles the creation of the S3 buckets, IAM role, Lambda function, and necessary permissions and notifications. Whenever a new file is uploaded to the source S3 bucket, the Lambda function will trigger an AWS Glue job to transform the data and store it in the target S3 bucket.


# Step-by-Step Guide for Real-time Stream Processing with AWS Lambda and Kinesis

This guide will walk you through setting up a real-time stream processing pipeline using AWS Lambda and Kinesis. We will cover the following steps:

1. **Setting Up the Environment**
2. **Creating a Kinesis Stream**
3. **Setting Up IAM Roles**
4. **Creating and Deploying a Lambda Function**
5. **Configuring Kinesis to Trigger Lambda**
6. **Testing the Setup**

## 1. Setting Up the Environment

### Prerequisites
- AWS Account
- AWS CLI installed and configured
- Terraform installed

## 2. Creating a Kinesis Stream

### Step 1: Create a Kinesis Stream
1. Log in to the AWS Management Console.
2. Navigate to the Kinesis service.
3. Click on "Create data stream".
4. Enter a stream name (e.g., `my-kinesis-stream`).
5. Set the number of shards (e.g., 1 for simplicity).
6. Click on "Create data stream".

## 3. Setting Up IAM Roles

### Step 2: Create IAM Roles
1. Go to the IAM console.
2. Click on "Roles" in the left sidebar.
3. Click on "Create role".
4. Choose "AWS service" and select "Lambda".
5. Click on "Next: Permissions".
6. Attach the following policies:
   - `AWSLambdaBasicExecutionRole`
   - `AmazonKinesisReadOnlyAccess`
7. Click on "Next: Tags", then "Next: Review".
8. Enter a role name (e.g., `LambdaKinesisAccessRole`).
9. Click on "Create role".

## 4. Creating and Deploying a Lambda Function

### Step 3: Create a Lambda Function
1. Navigate to the AWS Lambda console.
2. Click on "Create function".
3. Choose "Author from scratch".
4. Configure the following settings:
   - Function name: `StreamProcessorLambda`
   - Runtime: Python 3.x (or any other supported runtime)
   - Role: Choose the IAM role created earlier (`LambdaKinesisAccessRole`)
5. Click on "Create function".

### Step 4: Write the Lambda Function Code
Create a file named `stream_processor_lambda.py` with the following content:

```python
import json

def lambda_handler(event, context):
    for record in event['Records']:
        # Decode the Kinesis data
        payload = record['kinesis']['data']
        decoded_payload = base64.b64decode(payload).decode('utf-8')
        
        # Process the payload (for demonstration, we'll just print it)
        print(f"Decoded payload: {decoded_payload}")
        
        # You can add more processing logic here

    return {
        'statusCode': 200,
        'body': json.dumps('Processing completed')
    }
```

### Step 5: Create a Deployment Package
Zip the `stream_processor_lambda.py` file into a deployment package:

```bash
zip stream_processor_lambda.zip stream_processor_lambda.py
```

### Step 6: Deploy the Lambda Function
1. Upload the deployment package to the Lambda function.
2. Click on "Deploy".

## 5. Configuring Kinesis to Trigger Lambda

### Step 7: Set Up Kinesis Trigger
1. Navigate to the AWS Lambda console.
2. Select your Lambda function (`StreamProcessorLambda`).
3. Click on the "Add trigger" button.
4. Select "Kinesis" from the list of trigger sources.
5. Configure the following settings:
   - Kinesis stream: Choose the Kinesis stream created earlier (`my-kinesis-stream`).
   - Batch size: 100 (default)
   - Starting position: Latest
6. Click on "Add".

## 6. Testing the Setup

### Step 8: Put Records into Kinesis Stream
Use the AWS CLI to put records into the Kinesis stream:

```bash
aws kinesis put-record --stream-name my-kinesis-stream --partition-key "partitionKey" --data "Hello, Kinesis!"
aws kinesis put-record --stream-name my-kinesis-stream --partition-key "partitionKey" --data "This is a test message."
```

### Step 9: Verify Lambda Execution
1. Go to the AWS Lambda console.
2. Select your Lambda function (`StreamProcessorLambda`).
3. Click on the "Monitor" tab and then "View logs in CloudWatch".
4. Check the CloudWatch logs to see the output of your Lambda function. You should see logs indicating that the payloads were decoded and printed.

## Terraform Script

### Step 10: Create the Terraform Configuration File

Create a file named `main.tf` and add the following content:

```hcl
provider "aws" {
  region = "us-east-1"  # Change to your preferred region
}

resource "aws_kinesis_stream" "kinesis_stream" {
  name             = "my-kinesis-stream"
  shard_count      = 1
  retention_period = 24
}

resource "aws_iam_role" "lambda_kinesis_role" {
  name = "lambda_kinesis_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Effect    = "Allow"
      Sid       = ""
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_kinesis_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "kinesis_read_access" {
  role       = aws_iam_role.lambda_kinesis_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonKinesisReadOnlyAccess"
}

resource "aws_lambda_function" "stream_processor_lambda" {
  function_name = "StreamProcessorLambda"
  role          = aws_iam_role.lambda_kinesis_role.arn
  handler       = "stream_processor_lambda.lambda_handler"
  runtime       = "python3.8"
  
  filename = "stream_processor_lambda.zip"

  source_code_hash = filebase64sha256("stream_processor_lambda.zip")
}

resource "aws_lambda_event_source_mapping" "kinesis_trigger" {
  event_source_arn  = aws_kinesis_stream.kinesis_stream.arn
  function_name     = aws_lambda_function.stream_processor_lambda.arn
  starting_position = "LATEST"
  batch_size        = 100
}

output "kinesis_stream_name" {
  value = aws_kinesis_stream.kinesis_stream.name
}

output "lambda_function_name" {
  value = aws_lambda_function.stream_processor_lambda.function_name
}
```

### Summary

By following these steps, you have set up a real-time stream processing pipeline using AWS Lambda and Kinesis. The Terraform script handles the creation of the Kinesis stream, IAM role, Lambda function, and necessary permissions and triggers. Whenever a new record is put into the Kinesis stream, the Lambda function will be triggered to process the record.
