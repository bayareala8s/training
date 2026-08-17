Certainly! Here's a step-by-step guide on integrating AWS API Gateway with AWS Lambda:

### Step 1: Create an AWS Account
If you don't have an AWS account, [create one](https://aws.amazon.com/).

### Step 2: Create a Lambda Function
1. **Navigate to the Lambda Console**:
   - Go to the AWS Management Console.
   - Select "Lambda" from the Services menu.

2. **Create a Function**:
   - Click on "Create function".
   - Choose "Author from scratch".
   - Function name: `MyLambdaFunction`.
   - Runtime: Choose your preferred runtime (e.g., Python 3.x, Node.js, etc.).
   - Click "Create function".

3. **Configure the Lambda Function**:
   - In the function code section, write your Lambda function code. For example, in Python:
     ```python
     def lambda_handler(event, context):
         return {
             'statusCode': 200,
             'body': 'Hello from Lambda!'
         }
     ```
   - Click "Deploy".

### Step 3: Create an API in API Gateway
1. **Navigate to the API Gateway Console**:
   - Go to the AWS Management Console.
   - Select "API Gateway" from the Services menu.

2. **Create an API**:
   - Click "Create API".
   - Choose "REST API" and click "Build".

3. **Configure the API**:
   - API name: `MyAPIGateway`.
   - Click "Create API".

### Step 4: Create a Resource and Method
1. **Create a Resource**:
   - In the API Gateway console, select your API (`MyAPIGateway`).
   - In the left-hand pane, click on "Resources".
   - Click "Create Resource".
   - Resource name: `myresource`.
   - Resource path: `/myresource`.
   - Click "Create Resource".

2. **Create a Method**:
   - With `/myresource` selected, click "Create Method".
   - Select "GET" from the dropdown and click the checkmark.

3. **Set Up the Integration Request**:
   - Integration type: Select "Lambda Function".
   - Use Lambda Proxy Integration: Check the box.
   - Lambda Region: Select your region.
   - Lambda Function: Enter `MyLambdaFunction`.
   - Click "Save".
   - Confirm the necessary permissions by clicking "OK".

### Step 5: Deploy the API
1. **Create a Deployment Stage**:
   - In the API Gateway console, click "Actions".
   - Select "Deploy API".
   - Deployment stage: Select "[New Stage]".
   - Stage name: `dev`.
   - Click "Deploy".

2. **Get the Invoke URL**:
   - After deployment, you will see the invoke URL for your API. It will look something like `https://<api-id>.execute-api.<region>.amazonaws.com/dev`.

### Step 6: Test the API
1. **Invoke the API**:
   - Open your web browser or use a tool like Postman or curl.
   - Make a GET request to the invoke URL: `https://<api-id>.execute-api.<region>.amazonaws.com/dev/myresource`.

2. **Verify the Response**:
   - You should receive a response from the Lambda function: `Hello from Lambda!`.

### Additional Configuration (Optional)
1. **Set Up CORS**:
   - In the API Gateway console, select your method (GET).
   - Click "Method Response".
   - Add a 200 status response.
   - Click "Method Request".
   - Click "Add header" and add `Access-Control-Allow-Origin`.
   - Deploy the API again.

2. **Enable Detailed Logging**:
   - Go to "Stages" in the API Gateway console.
   - Select your stage (`dev`).
   - Click on "Logs/Tracing".
   - Enable CloudWatch Logs.

3. **Custom Domain Name**:
   - In the API Gateway console, go to "Custom Domain Names".
   - Click "Create Custom Domain Name".
   - Follow the steps to set up a custom domain.

4. **Set Up API Keys and Usage Plans**:
   - In the API Gateway console, go to "API Keys".
   - Click "Create API Key".
   - Follow the steps to create and configure usage plans.

### Summary
You've successfully created an API Gateway, integrated it with a Lambda function, deployed it, and tested the API. You can further enhance your setup with additional configurations like CORS, logging, custom domain names, and API keys.

Feel free to ask if you need more detailed information on any step or additional configurations.


Certainly! Below are detailed real-world examples of integrating AWS API Gateway with AWS Lambda using Terraform scripts.

### Example 1: Basic API Gateway and Lambda Integration

#### Terraform Script

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_iam_role" "lambda_execution" {
  name = "lambda_execution_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "lambda_policy" {
  name       = "lambda_policy"
  roles      = [aws_iam_role.lambda_execution.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "my_lambda" {
  function_name = "MyLambdaFunction"
  role          = aws_iam_role.lambda_execution.arn
  handler       = "index.handler"
  runtime       = "nodejs14.x"
  filename      = "lambda_function_payload.zip"

  source_code_hash = filebase64sha256("lambda_function_payload.zip")
}

resource "aws_api_gateway_rest_api" "my_api" {
  name        = "MyAPIGateway"
  description = "API Gateway for my Lambda function"
}

resource "aws_api_gateway_resource" "my_resource" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  parent_id   = aws_api_gateway_rest_api.my_api.root_resource_id
  path_part   = "myresource"
}

resource "aws_api_gateway_method" "get_method" {
  rest_api_id   = aws_api_gateway_rest_api.my_api.id
  resource_id   = aws_api_gateway_resource.my_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  resource_id = aws_api_gateway_resource.my_resource.id
  http_method = aws_api_gateway_method.get_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.my_lambda.invoke_arn
}

resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.my_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "api_deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda_integration,
  ]
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  stage_name  = "dev"
}
```

#### Lambda Function Code (`index.js`)

```javascript
exports.handler = async (event) => {
    const response = {
        statusCode: 200,
        body: JSON.stringify('Hello from Lambda!'),
    };
    return response;
};
```

#### Packaging and Deploying
1. Create a zip file of the Lambda function:
   ```sh
   zip lambda_function_payload.zip index.js
   ```

2. Apply the Terraform script:
   ```sh
   terraform init
   terraform apply
   ```

### Example 2: API Gateway with Lambda and DynamoDB

#### Terraform Script

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_iam_role" "lambda_execution" {
  name = "lambda_execution_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "lambda_policy" {
  name       = "lambda_policy"
  roles      = [aws_iam_role.lambda_execution.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_dynamodb_table" "my_table" {
  name         = "MyTable"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "ID"

  attribute {
    name = "ID"
    type = "S"
  }
}

resource "aws_lambda_function" "my_lambda" {
  function_name = "MyLambdaFunction"
  role          = aws_iam_role.lambda_execution.arn
  handler       = "index.handler"
  runtime       = "nodejs14.x"
  filename      = "lambda_function_payload.zip"
  
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.my_table.name
    }
  }

  source_code_hash = filebase64sha256("lambda_function_payload.zip")
}

resource "aws_api_gateway_rest_api" "my_api" {
  name        = "MyAPIGateway"
  description = "API Gateway for my Lambda function"
}

resource "aws_api_gateway_resource" "my_resource" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  parent_id   = aws_api_gateway_rest_api.my_api.root_resource_id
  path_part   = "myresource"
}

resource "aws_api_gateway_method" "get_method" {
  rest_api_id   = aws_api_gateway_rest_api.my_api.id
  resource_id   = aws_api_gateway_resource.my_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  resource_id = aws_api_gateway_resource.my_resource.id
  http_method = aws_api_gateway_method.get_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.my_lambda.invoke_arn
}

resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.my_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "api_deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda_integration,
  ]
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  stage_name  = "dev"
}
```

#### Lambda Function Code (`index.js`)

```javascript
const AWS = require('aws-sdk');
const dynamo = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const params = {
        TableName: process.env.TABLE_NAME,
        Item: {
            ID: '1',
            Message: 'Hello from DynamoDB'
        }
    };

    await dynamo.put(params).promise();

    const response = {
        statusCode: 200,
        body: JSON.stringify('Data inserted into DynamoDB'),
    };
    return response;
};
```

#### Packaging and Deploying
1. Create a zip file of the Lambda function:
   ```sh
   zip lambda_function_payload.zip index.js
   ```

2. Apply the Terraform script:
   ```sh
   terraform init
   terraform apply
   ```

### Summary
These examples demonstrate how to set up AWS API Gateway and Lambda integration using Terraform. The first example is a basic integration, while the second example includes interaction with DynamoDB. By following these examples, you can build and deploy robust serverless applications on AWS.
