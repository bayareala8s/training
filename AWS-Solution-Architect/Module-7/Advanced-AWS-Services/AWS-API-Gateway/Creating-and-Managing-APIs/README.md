### Step-by-Step Guide on Creating and Managing APIs with AWS API Gateway

#### Step 1: Setting Up AWS API Gateway

1. **Sign in to AWS Management Console**
   - Navigate to [AWS Management Console](https://aws.amazon.com/console/).
   - Sign in with your AWS account credentials.

2. **Navigate to API Gateway**
   - In the AWS Management Console, search for "API Gateway" in the services search bar.
   - Click on "API Gateway" to open the service.

#### Step 2: Creating a New API

1. **Choose API Type**
   - Click on "Create API."
   - Choose between REST API, WebSocket API, or HTTP API. For this guide, we will use the REST API.
   - Click on "Build."

2. **Define API**
   - Select "New API."
   - Enter an API name (e.g., "MyFirstAPI").
   - Provide a description (optional).
   - Choose an endpoint type: Edge Optimized, Regional, or Private.
   - Click on "Create API."

#### Step 3: Creating Resources and Methods

1. **Create a Resource**
   - In the API Gateway console, click on "Resources" in the left-hand menu.
   - Click on "Actions" and select "Create Resource."
   - Enter a resource name (e.g., "users") and a resource path (e.g., "/users").
   - Click on "Create Resource."

2. **Create a Method**
   - Select the resource you just created (e.g., /users).
   - Click on "Actions" and select "Create Method."
   - Choose an HTTP method (e.g., GET, POST).
   - Click on the checkmark to proceed.

3. **Configure Method Integration**
   - Select "Integration Type" (e.g., Lambda Function, HTTP, Mock, AWS Service, VPC Link).
   - For this guide, choose "Lambda Function."
   - Use the Lambda function you want to integrate with the API.
   - Click on "Save."
   - Confirm that you want to give API Gateway permission to invoke your Lambda function.

#### Step 4: Deploying the API

1. **Create a Deployment Stage**
   - Click on "Actions" and select "Deploy API."
   - Create a new deployment stage (e.g., "prod").
   - Click on "Deploy."

2. **Invoke the API**
   - After deployment, you will receive an Invoke URL.
   - Use this URL to test your API (e.g., via a web browser or tools like Postman).

#### Step 5: Configuring API Gateway Settings

1. **Enable CORS**
   - Select the method (e.g., GET) under the resource (e.g., /users).
   - Click on "Actions" and select "Enable CORS."
   - Configure the necessary CORS settings and click on "Enable CORS and replace existing CORS headers."

2. **Logging and Monitoring**
   - Navigate to "Stages" in the left-hand menu.
   - Select the deployment stage (e.g., prod).
   - Click on the "Logs/Tracing" tab.
   - Enable CloudWatch Logs and X-Ray tracing if needed.

3. **API Keys and Usage Plans**
   - Navigate to "API Keys" in the left-hand menu.
   - Click on "Create API Key."
   - Associate the API key with a usage plan.
   - Configure throttling and quota limits as needed.

#### Step 6: Securing Your API

1. **Authentication and Authorization**
   - Configure IAM roles and policies to control access to your API.
   - Integrate with Amazon Cognito for user authentication and authorization.

2. **Custom Domain Names**
   - Set up custom domain names for your API.
   - Navigate to "Custom Domain Names" in the left-hand menu.
   - Click on "Create Custom Domain Name" and follow the instructions.

3. **Throttling and Quotas**
   - Set up usage plans and API keys to manage API throttling and quotas.
   - Navigate to "Usage Plans" in the left-hand menu.
   - Create a new usage plan and associate it with your API and API keys.

#### Step 7: Managing and Monitoring APIs

1. **Monitoring with CloudWatch**
   - Navigate to the "Stages" section.
   - Select the stage (e.g., prod).
   - Click on the "Logs/Tracing" tab.
   - Enable CloudWatch Logs to monitor API metrics.

2. **Usage Analytics**
   - Use CloudWatch metrics to monitor API calls, latency, and error rates.
   - Set up CloudWatch Alarms to get notified of threshold breaches.

3. **API Versioning**
   - Manage different versions of your API.
   - Use stages to deploy different versions (e.g., v1, v2).

4. **Documentation**
   - Generate and manage API documentation.
   - Use the "Documentation" section to add detailed descriptions of API resources and methods.

5. **Updating APIs**
   - Make changes to your API by modifying resources, methods, or integrations.
   - Redeploy the API to the appropriate stage after making changes.

### Conclusion

This step-by-step guide provides an overview of creating, deploying, and managing APIs using AWS API Gateway. By following these steps, you can set up secure, scalable, and well-documented APIs that integrate seamlessly with your backend services. For more advanced configurations and detailed information, refer to the [AWS API Gateway documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html).



### Real-World Examples of Using AWS API Gateway

#### Example 1: Serverless Web Application Backend

**Scenario:**
A startup company is developing a web application for task management. They want to use a serverless architecture to minimize operational overhead and scale automatically with user demand.

**Solution:**
- **Frontend:** React.js hosted on Amazon S3 and served via Amazon CloudFront.
- **Backend:** AWS API Gateway, AWS Lambda, Amazon DynamoDB.

**Steps:**
1. **Create API Gateway:**
   - Define a REST API for the application.
   - Create resources and methods for handling tasks (e.g., `/tasks` with methods GET, POST, PUT, DELETE).

2. **Integrate with Lambda:**
   - Use Lambda functions to handle the business logic for each method (e.g., fetching tasks, creating tasks).
   - Connect API Gateway methods to the corresponding Lambda functions.

3. **Database Setup:**
   - Use DynamoDB to store task data.
   - Lambda functions interact with DynamoDB to perform CRUD operations.

4. **Deploy and Secure:**
   - Deploy the API to different stages (e.g., dev, test, prod).
   - Use Amazon Cognito for user authentication and authorization.
   - Enable CORS to allow frontend access to the API.

5. **Monitoring and Maintenance:**
   - Enable CloudWatch for monitoring API performance and errors.
   - Set up alarms to notify the team of any issues.

**Outcome:**
The startup has a fully serverless backend that scales automatically, requires minimal maintenance, and integrates seamlessly with their frontend application.

#### Example 2: Microservices Architecture for E-commerce Platform

**Scenario:**
An e-commerce company wants to migrate its monolithic application to a microservices architecture to improve scalability, maintainability, and deployment flexibility.

**Solution:**
- **Microservices:** Deployed using Amazon ECS or EKS.
- **API Gateway:** Acts as a gateway for all microservices.
- **Authentication:** Amazon Cognito or custom Lambda authorizers.
- **Database:** Amazon RDS for relational data, Amazon DynamoDB for NoSQL data.

**Steps:**
1. **Create API Gateway:**
   - Define a REST API to route requests to different microservices.
   - Create resources for different services (e.g., `/products`, `/orders`, `/users`).

2. **Integration with Microservices:**
   - Use HTTP integrations to route requests from API Gateway to the respective microservices running on ECS or EKS.
   - Define request and response mappings to ensure consistent API contracts.

3. **Authentication and Authorization:**
   - Implement Amazon Cognito for user authentication.
   - Use JWT tokens to secure API requests and control access to different endpoints.

4. **Deploy and Versioning:**
   - Deploy the API to different stages (e.g., dev, staging, prod).
   - Use API Gateway versioning to manage and deploy different versions of the API.

5. **Monitoring and Scaling:**
   - Enable CloudWatch for monitoring API usage, performance, and error rates.
   - Set up auto-scaling for microservices based on demand.

**Outcome:**
The e-commerce platform now has a microservices architecture that is highly scalable, easy to maintain, and allows for independent deployment of services. API Gateway provides a unified interface for all microservices, enhancing the overall flexibility and robustness of the application.

#### Example 3: Real-time Chat Application

**Scenario:**
A social media company wants to add a real-time chat feature to their application to enhance user engagement.

**Solution:**
- **Frontend:** Web and mobile clients using WebSocket.
- **Backend:** AWS API Gateway (WebSocket API), AWS Lambda, Amazon DynamoDB.

**Steps:**
1. **Create WebSocket API:**
   - Define a WebSocket API in API Gateway.
   - Create routes for different chat actions (e.g., `$connect`, `$disconnect`, `sendMessage`).

2. **Lambda Integrations:**
   - Implement Lambda functions to handle WebSocket connections, disconnections, and messages.
   - Connect WebSocket routes to the respective Lambda functions.

3. **Database and Messaging:**
   - Use DynamoDB to store chat messages and user connection information.
   - Lambda functions interact with DynamoDB to manage chat data.

4. **Deploy and Secure:**
   - Deploy the WebSocket API to different stages (e.g., dev, staging, prod).
   - Implement authentication using Amazon Cognito to ensure only authenticated users can connect to the WebSocket API.

5. **Monitoring and Scaling:**
   - Enable CloudWatch for monitoring WebSocket connections and messages.
   - Use AWS Lambda auto-scaling to handle varying loads.

**Outcome:**
The social media company successfully adds a real-time chat feature to their application, enhancing user engagement. The WebSocket API scales automatically to handle a large number of concurrent users and messages, providing a seamless chat experience.

#### Example 4: IoT Data Ingestion and Processing

**Scenario:**
A manufacturing company wants to collect and process data from IoT devices in their factories for real-time monitoring and analytics.

**Solution:**
- **IoT Devices:** Connected via MQTT to AWS IoT Core.
- **API Gateway:** For external applications to access processed IoT data.
- **Backend:** AWS Lambda, Amazon Kinesis, Amazon S3.

**Steps:**
1. **Set Up IoT Core:**
   - Connect IoT devices to AWS IoT Core using MQTT.
   - Define IoT rules to route incoming data to Kinesis streams.

2. **Create API Gateway:**
   - Define a REST API to provide access to processed IoT data.
   - Create resources and methods for querying data (e.g., `/sensorData` with GET method).

3. **Lambda Integrations:**
   - Implement Lambda functions to process data from Kinesis streams and store results in S3 or DynamoDB.
   - Connect API Gateway methods to Lambda functions that query the processed data.

4. **Deploy and Secure:**
   - Deploy the API to different stages (e.g., dev, prod).
   - Implement API keys and usage plans to control access to the API.

5. **Monitoring and Analytics:**
   - Use CloudWatch to monitor API usage and performance.
   - Set up Amazon QuickSight for data visualization and analytics.

**Outcome:**
The manufacturing company can now collect, process, and analyze IoT data in real-time. External applications can access processed data via API Gateway, enabling advanced monitoring and analytics capabilities.

### Conclusion

These real-world examples illustrate how AWS API Gateway can be used to build scalable, secure, and maintainable APIs for a variety of applications, from serverless backends and microservices to real-time applications and IoT data processing. By leveraging AWS API Gateway and other AWS services, organizations can quickly develop robust APIs that meet their specific needs.


Here is a Terraform script to create a serverless web application backend using AWS API Gateway, AWS Lambda, and Amazon DynamoDB.

### Prerequisites
- Install [Terraform](https://www.terraform.io/downloads.html)
- AWS CLI configured with appropriate IAM permissions
- Basic understanding of Terraform and AWS services

### Terraform Configuration

#### Step 1: Create a `main.tf` file

```hcl
provider "aws" {
  region = "us-west-2"  # Specify your AWS region
}

resource "aws_dynamodb_table" "tasks" {
  name           = "tasks"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "taskId"
  attribute {
    name = "taskId"
    type = "S"
  }
  tags = {
    Name = "tasks-table"
  }
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
  ]
}

resource "aws_lambda_function" "tasks_lambda" {
  filename         = "lambda_function.zip"  # Path to your Lambda deployment package
  function_name    = "tasks_lambda"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "index.handler"  # Update with your handler name
  runtime          = "nodejs14.x"  # Update with your runtime
  source_code_hash = filebase64sha256("lambda_function.zip")

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.tasks.name
    }
  }
}

resource "aws_api_gateway_rest_api" "api" {
  name        = "tasks_api"
  description = "API for tasks management"
}

resource "aws_api_gateway_resource" "tasks_resource" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "tasks"
}

resource "aws_api_gateway_method" "tasks_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.tasks_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.tasks_resource.id
  http_method = aws_api_gateway_method.tasks_method.http_method
  type        = "AWS_PROXY"
  integration_http_method = "POST"
  uri         = aws_lambda_function.tasks_lambda.invoke_arn
}

resource "aws_api_gateway_deployment" "api_deployment" {
  depends_on = [aws_api_gateway_integration.lambda_integration]
  rest_api_id = aws_api_gateway_rest_api.api.id
  stage_name  = "prod"
}

resource "aws_lambda_permission" "api_gateway_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.tasks_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}

output "api_endpoint" {
  value = "${aws_api_gateway_deployment.api_deployment.invoke_url}/tasks"
}
```

#### Step 2: Prepare the Lambda Function

Create a simple Node.js Lambda function and package it into a ZIP file named `lambda_function.zip`.

**index.js:**

```javascript
const AWS = require('aws-sdk');
const dynamo = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
  const body = JSON.parse(event.body);
  const taskId = body.taskId;
  const taskDescription = body.taskDescription;

  const params = {
    TableName: process.env.TABLE_NAME,
    Item: {
      taskId: taskId,
      taskDescription: taskDescription
    }
  };

  try {
    await dynamo.put(params).promise();
    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'Task created successfully' })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Could not create task' })
    };
  }
};
```

Create the ZIP file:

```bash
zip -r lambda_function.zip index.js node_modules
```

#### Step 3: Initialize Terraform and Apply

Run the following commands in your terminal:

```bash
terraform init
terraform apply
```

### Conclusion

This Terraform script sets up a serverless web application backend with AWS API Gateway, AWS Lambda, and Amazon DynamoDB. The Lambda function handles creating tasks and storing them in DynamoDB, while API Gateway provides a RESTful interface for the application.

This example can be extended with additional methods (e.g., GET, PUT, DELETE) and more complex business logic as needed.


Here is a Terraform script to create a microservices architecture for an e-commerce platform using AWS API Gateway, AWS Lambda, and Amazon RDS.

### Prerequisites
- Install [Terraform](https://www.terraform.io/downloads.html)
- AWS CLI configured with appropriate IAM permissions
- Basic understanding of Terraform and AWS services

### Terraform Configuration

#### Step 1: Create a `main.tf` file

```hcl
provider "aws" {
  region = "us-west-2"  # Specify your AWS region
}

# VPC Setup
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "subnet1" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "us-west-2a"
}

resource "aws_subnet" "subnet2" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "us-west-2b"
}

# Security Group
resource "aws_security_group" "lambda_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# RDS Setup
resource "aws_db_instance" "db" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  name                 = "ecommerce"
  username             = "admin"
  password             = "password"
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true

  vpc_security_group_ids = [aws_security_group.lambda_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  publicly_accessible = true
}

resource "aws_db_subnet_group" "main" {
  name       = "main"
  subnet_ids = [aws_subnet.subnet1.id, aws_subnet.subnet2.id]

  tags = {
    Name = "Main DB Subnet Group"
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    "arn:aws:iam::aws:policy/AmazonRDSFullAccess",
  ]
}

# Lambda Functions
resource "aws_lambda_function" "products_lambda" {
  filename         = "products_lambda.zip"  # Path to your Lambda deployment package
  function_name    = "products_lambda"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "index.handler"  # Update with your handler name
  runtime          = "nodejs14.x"  # Update with your runtime
  source_code_hash = filebase64sha256("products_lambda.zip")

  environment {
    variables = {
      DB_HOST     = aws_db_instance.db.address
      DB_NAME     = "ecommerce"
      DB_USER     = "admin"
      DB_PASSWORD = "password"
    }
  }
}

resource "aws_lambda_function" "orders_lambda" {
  filename         = "orders_lambda.zip"  # Path to your Lambda deployment package
  function_name    = "orders_lambda"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "index.handler"  # Update with your handler name
  runtime          = "nodejs14.x"  # Update with your runtime
  source_code_hash = filebase64sha256("orders_lambda.zip")

  environment {
    variables = {
      DB_HOST     = aws_db_instance.db.address
      DB_NAME     = "ecommerce"
      DB_USER     = "admin"
      DB_PASSWORD = "password"
    }
  }
}

# API Gateway Setup
resource "aws_api_gateway_rest_api" "api" {
  name        = "ecommerce_api"
  description = "API for e-commerce platform"
}

# Products Resource
resource "aws_api_gateway_resource" "products_resource" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "products"
}

resource "aws_api_gateway_method" "products_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.products_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "products_integration" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.products_resource.id
  http_method = aws_api_gateway_method.products_method.http_method
  type        = "AWS_PROXY"
  integration_http_method = "POST"
  uri         = aws_lambda_function.products_lambda.invoke_arn
}

# Orders Resource
resource "aws_api_gateway_resource" "orders_resource" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "orders"
}

resource "aws_api_gateway_method" "orders_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.orders_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "orders_integration" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.orders_resource.id
  http_method = aws_api_gateway_method.orders_method.http_method
  type        = "AWS_PROXY"
  integration_http_method = "POST"
  uri         = aws_lambda_function.orders_lambda.invoke_arn
}

# Deployment
resource "aws_api_gateway_deployment" "api_deployment" {
  depends_on = [
    aws_api_gateway_integration.products_integration,
    aws_api_gateway_integration.orders_integration
  ]
  rest_api_id = aws_api_gateway_rest_api.api.id
  stage_name  = "prod"
}

resource "aws_lambda_permission" "api_gateway_invoke_products" {
  statement_id  = "AllowAPIGatewayInvokeProducts"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.products_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "api_gateway_invoke_orders" {
  statement_id  = "AllowAPIGatewayInvokeOrders"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.orders_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}

output "api_endpoint" {
  value = "${aws_api_gateway_deployment.api_deployment.invoke_url}"
}
```

#### Step 2: Prepare the Lambda Functions

Create two simple Node.js Lambda functions and package them into ZIP files named `products_lambda.zip` and `orders_lambda.zip`.

**products_lambda/index.js:**

```javascript
const mysql = require('mysql');

const db = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
});

exports.handler = async (event) => {
  const promise = new Promise((resolve, reject) => {
    db.query('SELECT * FROM products', (error, results) => {
      if (error) {
        reject(error);
      } else {
        resolve(results);
      }
    });
  });

  try {
    const results = await promise;
    return {
      statusCode: 200,
      body: JSON.stringify(results)
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Could not retrieve products' })
    };
  }
};
```

**orders_lambda/index.js:**

```javascript
const mysql = require('mysql');

const db = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
});

exports.handler = async (event) => {
  const body = JSON.parse(event.body);
  const { productId, quantity } = body;

  const promise = new Promise((resolve, reject) => {
    const query = 'INSERT INTO orders (productId, quantity) VALUES (?, ?)';
    db.query(query, [productId, quantity], (error, results) => {
      if (error) {
        reject(error);
      } else {
        resolve(results);
      }
    });
  });

  try {
    const results =

 await promise;
    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'Order created successfully' })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Could not create order' })
    };
  }
};
```

Create the ZIP files:

```bash
# For products_lambda
zip -r products_lambda.zip index.js node_modules

# For orders_lambda
zip -r orders_lambda.zip index.js node_modules
```

#### Step 3: Initialize Terraform and Apply

Run the following commands in your terminal:

```bash
terraform init
terraform apply
```

### Conclusion

This Terraform script sets up a microservices architecture for an e-commerce platform using AWS API Gateway, AWS Lambda, and Amazon RDS. The script includes resources for creating a VPC, security groups, RDS instance, IAM roles, Lambda functions, and API Gateway resources. This example can be extended with additional microservices and more complex business logic as needed.


Here is a Terraform script to create a real-time chat application using AWS API Gateway (WebSocket API), AWS Lambda, and Amazon DynamoDB.

### Prerequisites
- Install [Terraform](https://www.terraform.io/downloads.html)
- AWS CLI configured with appropriate IAM permissions
- Basic understanding of Terraform and AWS services

### Terraform Configuration

#### Step 1: Create a `main.tf` file

```hcl
provider "aws" {
  region = "us-west-2"  # Specify your AWS region
}

# DynamoDB Table for storing WebSocket connection IDs
resource "aws_dynamodb_table" "connections" {
  name           = "connections"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "connectionId"
  attribute {
    name = "connectionId"
    type = "S"
  }
  tags = {
    Name = "connections-table"
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
    "arn:aws:iam::aws:policy/AmazonAPIGatewayInvokeFullAccess"
  ]
}

# Lambda Functions
resource "aws_lambda_function" "connect_lambda" {
  filename         = "connect_lambda.zip"  # Path to your Lambda deployment package
  function_name    = "connect_lambda"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "index.handler"  # Update with your handler name
  runtime          = "nodejs14.x"  # Update with your runtime
  source_code_hash = filebase64sha256("connect_lambda.zip")
}

resource "aws_lambda_function" "disconnect_lambda" {
  filename         = "disconnect_lambda.zip"  # Path to your Lambda deployment package
  function_name    = "disconnect_lambda"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "index.handler"  # Update with your handler name
  runtime          = "nodejs14.x"  # Update with your runtime
  source_code_hash = filebase64sha256("disconnect_lambda.zip")
}

resource "aws_lambda_function" "message_lambda" {
  filename         = "message_lambda.zip"  # Path to your Lambda deployment package
  function_name    = "message_lambda"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "index.handler"  # Update with your handler name
  runtime          = "nodejs14.x"  # Update with your runtime
  source_code_hash = filebase64sha256("message_lambda.zip")
}

# API Gateway WebSocket API
resource "aws_api_gatewayv2_api" "websocket_api" {
  name          = "websocket_chat_api"
  protocol_type = "WEBSOCKET"
  route_selection_expression = "$request.body.action"
}

# Routes and Integrations
resource "aws_api_gatewayv2_route" "connect_route" {
  api_id    = aws_api_gatewayv2_api.websocket_api.id
  route_key = "$connect"
  target    = "integrations/${aws_api_gatewayv2_integration.connect_integration.id}"
}

resource "aws_api_gatewayv2_route" "disconnect_route" {
  api_id    = aws_api_gatewayv2_api.websocket_api.id
  route_key = "$disconnect"
  target    = "integrations/${aws_api_gatewayv2_integration.disconnect_integration.id}"
}

resource "aws_api_gatewayv2_route" "message_route" {
  api_id    = aws_api_gatewayv2_api.websocket_api.id
  route_key = "sendMessage"
  target    = "integrations/${aws_api_gatewayv2_integration.message_integration.id}"
}

resource "aws_api_gatewayv2_integration" "connect_integration" {
  api_id           = aws_api_gatewayv2_api.websocket_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.connect_lambda.invoke_arn
}

resource "aws_api_gatewayv2_integration" "disconnect_integration" {
  api_id           = aws_api_gatewayv2_api.websocket_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.disconnect_lambda.invoke_arn
}

resource "aws_api_gatewayv2_integration" "message_integration" {
  api_id           = aws_api_gatewayv2_api.websocket_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.message_lambda.invoke_arn
}

# Deployment
resource "aws_api_gatewayv2_stage" "websocket_stage" {
  api_id      = aws_api_gatewayv2_api.websocket_api.id
  name        = "prod"
  deployment_id = aws_api_gatewayv2_deployment.websocket_deployment.id
}

resource "aws_api_gatewayv2_deployment" "websocket_deployment" {
  api_id = aws_api_gatewayv2_api.websocket_api.id
  depends_on = [
    aws_api_gatewayv2_integration.connect_integration,
    aws_api_gatewayv2_integration.disconnect_integration,
    aws_api_gatewayv2_integration.message_integration
  ]
}

# Lambda Permissions
resource "aws_lambda_permission" "allow_apigw_connect" {
  statement_id  = "AllowAPIGatewayInvokeConnect"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.connect_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gatewayv2_api.websocket_api.execution_arn}/*"
}

resource "aws_lambda_permission" "allow_apigw_disconnect" {
  statement_id  = "AllowAPIGatewayInvokeDisconnect"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.disconnect_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gatewayv2_api.websocket_api.execution_arn}/*"
}

resource "aws_lambda_permission" "allow_apigw_message" {
  statement_id  = "AllowAPIGatewayInvokeMessage"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.message_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gatewayv2_api.websocket_api.execution_arn}/*"
}

output "websocket_api_endpoint" {
  value = "${aws_api_gatewayv2_stage.websocket_stage.invoke_url}"
}
```

#### Step 2: Prepare the Lambda Functions

Create three simple Node.js Lambda functions and package them into ZIP files named `connect_lambda.zip`, `disconnect_lambda.zip`, and `message_lambda.zip`.

**connect_lambda/index.js:**

```javascript
const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
  const connectionId = event.requestContext.connectionId;
  
  const params = {
    TableName: 'connections',
    Item: {
      connectionId: connectionId
    }
  };
  
  try {
    await docClient.put(params).promise();
    return { statusCode: 200, body: 'Connected' };
  } catch (error) {
    return { statusCode: 500, body: 'Failed to connect: ' + JSON.stringify(error) };
  }
};
```

**disconnect_lambda/index.js:**

```javascript
const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
  const connectionId = event.requestContext.connectionId;

  const params = {
    TableName: 'connections',
    Key: {
      connectionId: connectionId
    }
  };

  try {
    await docClient.delete(params).promise();
    return { statusCode: 200, body: 'Disconnected' };
  } catch (error) {
    return { statusCode: 500, body: 'Failed to disconnect: ' + JSON.stringify(error) };
  }
};
```

**message_lambda/index.js:**

```javascript
const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient();
const apigwManagementApi = new AWS.ApiGatewayManagementApi({
  endpoint: process.env.API_ENDPOINT
});

exports.handler = async (event) => {
  const postData = JSON.parse(event.body).data;

  const params = {
    TableName: 'connections',
    ProjectionExpression: 'connectionId'
  };

  try {
    const data = await docClient.scan(params).promise();
    const postCalls = data.Items.map(async ({ connectionId }) => {
      try {
        await apigwManagementApi.postToConnection({ ConnectionId: connectionId, Data: postData }).promise();
      } catch (e) {
        if (e.statusCode === 410) {
          console.log(`Found stale connection, deleting ${connectionId}`);
          await docClient.delete({ TableName: 'connections', Key: { connectionId } }).promise();
        } else {
          throw e;
        }
      }
    });

    await Promise.all(postCalls);

    return { statusCode: 200, body: 'Data sent' };
  } catch (error) {
    return { statusCode: 500, body: 'Failed to send message: ' + JSON.stringify(error) };
  }
};
``

`

Create the ZIP files:

```bash
# For connect_lambda
zip -r connect_lambda.zip index.js node_modules

# For disconnect_lambda
zip -r disconnect_lambda.zip index.js node_modules

# For message_lambda
zip -r message_lambda.zip index.js node_modules
```

#### Step 3: Initialize Terraform and Apply

Run the following commands in your terminal:

```bash
terraform init
terraform apply
```

### Conclusion

This Terraform script sets up a real-time chat application using AWS API Gateway (WebSocket API), AWS Lambda, and Amazon DynamoDB. The script includes resources for creating DynamoDB tables, IAM roles, Lambda functions, and API Gateway resources. This example can be extended with additional functionality and more complex business logic as needed.
