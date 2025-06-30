Here's a **detailed Step-By-Step AWS File Transfer Architecture** to copy files **from multiple sources (on-prem SFTP and cloud S3 buckets)** to **multiple targets (cloud-hosted SFTP servers and S3 buckets)** using your preferred tech stack:
**AWS Transfer Family**, **S3**, **EventBridge**, **SQS**, **Step Functions**, **AWS Lambda (Python)**, and **DynamoDB**.

---

### ✅ **1. Architecture Overview**

```
 ┌─────────────┐       ┌────────────┐       ┌────────────────┐
 │ On-Prem SFTP│──────▶│ AWS Transfer│─────▶│ S3 Landing Zone│
 │   Servers   │       │   Family    │       │   (source)     │
 └─────────────┘       └────────────┘       └────────────────┘
                                               │
                                  ┌────────────┴────────────┐
                                  ▼                         ▼
                            EventBridge             Direct S3 Upload
                                  │                         │
                            ┌─────▼─────┐           ┌───────▼───────┐
                            │ SQS Queue │◀──────────┤  Cloud S3 Src │
                            └─────▲─────┘           └───────────────┘
                                  │
                             Step Functions
                                  │
                            ┌────▼────┐
                            │ Lambda  │  (Python logic to copy, tag, log)
                            └────┬────┘
                                 │
                ┌────────────────────────────────────┐
                ▼                                    ▼
      ┌────────────────┐                   ┌────────────────────┐
      │  S3 (Target)   │                   │ AWS Transfer Target│
      │  Bucket        │                   │  (Cloud SFTP Server│
      └────────────────┘                   └────────────────────┘

                ▼
        ┌──────────────┐
        │ DynamoDB Log │
        │  & Metadata  │
        └──────────────┘
```

---

## 🛠️ Step-by-Step Implementation

---

### **Step 1: Setup AWS Transfer Family for Source SFTP**

* **Use case**: On-prem SFTP clients upload files.
* **Action**:

  * Create AWS Transfer Family server (SFTP protocol).
  * Use **S3 bucket** as backend storage (landing zone).
  * Use **Identity provider (e.g., IAM or custom Lambda)** to authorize source SFTP users.
  * Create dedicated folder structure in S3:
    Example: `s3://file-landing-zone/from-sftp/clientX/`

---

### **Step 2: Enable Cloud S3 as Direct Source (Optional)**

* If files also land directly into S3 (not via Transfer Family), configure Event Notifications.

---

### **Step 3: Setup EventBridge Rule for File Arrival**

* **Trigger**: Object created in S3 landing zone.
* **Pattern**:

  * Source: `aws.s3`
  * Detail-type: `Object Created`
  * Bucket: `file-landing-zone`
* **Target**: SQS Queue (decouples file processing).

---

### **Step 4: Create SQS Queue**

* Holds file processing tasks.
* Use **message body** to include:

  ```json
  {
    "bucket": "file-landing-zone",
    "key": "from-sftp/clientX/filename.csv",
    "sourceType": "SFTP",
    "target": "s3://target-client-bucket",
    "targetType": "S3",
    "workflowId": "copy-sftp-to-s3",
    "customerId": "clientX"
  }
  ```

---

### **Step 5: Create Step Functions Workflow**

* Workflow triggered by new SQS messages.
* State Machine steps:

  1. **Read message**.
  2. **Run validation Lambda** (file format, naming, etc).
  3. **Route to Lambda based on source/target combination**.
  4. **Update DynamoDB with processing metadata**.
  5. **Trigger final notification or webhook (optional)**.

---

### **Step 6: Create AWS Lambda Functions (Python)**

Each Lambda handles one workflow pattern:

#### a. `lambda_sftp_to_s3.py`:

* Read file from S3 landing zone (uploaded via AWS Transfer).
* Copy to destination S3 bucket (via `boto3.copy_object`).

#### b. `lambda_s3_to_sftp.py`:

* Pull from source S3.
* Upload to SFTP using **Transfer Family Upload**:

  * Use `start-file-transfer` API or pre-write to S3 backend of Transfer Family.

#### c. `lambda_sftp_to_sftp.py`:

* Pull from S3 (uploaded via source Transfer Family).
* Write to target Transfer Family server backend S3 bucket.
* Mark status in DynamoDB.

#### d. `lambda_log_status.py`:

* Update **DynamoDB table** for:

  * File ID
  * Source
  * Target
  * Timestamp
  * Status (e.g., SUCCESS, FAILED)
  * Retry count

---

### **Step 7: Create DynamoDB Table**

* **Table Name**: `FileTransferTracking`
* **Partition key**: `workflowId`
* **Sort key**: `timestamp`
* Additional attributes: `source`, `target`, `status`, `retryCount`, `s3ObjectKey`

---

### **Step 8: Monitoring & Retry Logic**

* Use **Step Function Retry policies**.
* Add DLQ to SQS if messages fail after retries.
* Create **CloudWatch Alarms** on:

  * Lambda errors
  * Step Function failures
  * SQS queue depth

---

### **Step 9: Optional Add-ons**

* **Email/SNS Notification** upon job success/failure.
* **UI layer** for:

  * Uploads
  * Tracking status
  * Triggering manual re-processing

---

## 📂 Workflow Examples

| Source Type | Target Type | Lambda Workflow          |
| ----------- | ----------- | ------------------------ |
| SFTP        | S3          | `lambda_sftp_to_s3.py`   |
| S3          | SFTP        | `lambda_s3_to_sftp.py`   |
| SFTP        | SFTP        | `lambda_sftp_to_sftp.py` |
| S3          | S3          | `lambda_s3_to_s3.py`     |








++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


Here's a **detailed Step-by-Step guide for Step 5: Creating the Step Functions Workflow** for your AWS File Transfer architecture.

---

## ✅ **Step 5: Create Step Functions Workflow**

### 🎯 Goal:

Orchestrate file copy logic from the **SQS-triggered message** using **Python Lambdas**, while handling routing, validation, logging, and error management.

---

## 🔧 **Step-by-Step Setup**

---

### **Step 5.1: Define the Workflow Logic**

**Overview:**

1. **Receive SQS message**
2. **Validate Input**
3. **Route to correct Lambda (based on source/target type)**
4. **Invoke the correct Copy Lambda**
5. **Log success/failure to DynamoDB**
6. **Handle errors and retries**

---

### **Step 5.2: Sample Workflow Logic (Visual)**

```
[Start]
   │
   ▼
[Validate Input]
   │
   ▼
[Determine Route]
   ├─────────────▶ [SFTP → S3 Lambda]
   ├─────────────▶ [S3 → SFTP Lambda]
   ├─────────────▶ [SFTP → SFTP Lambda]
   └─────────────▶ [S3 → S3 Lambda]
   │
   ▼
[Log Result in DynamoDB]
   │
   ▼
[Success / End]
```

---

### **Step 5.3: Create IAM Role for Step Functions**

Attach the following permissions to a new IAM role:

```json
{
  "Effect": "Allow",
  "Action": [
    "lambda:InvokeFunction",
    "sqs:ReceiveMessage",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem",
    "states:StartExecution"
  ],
  "Resource": "*"
}
```

---

### **Step 5.4: Define State Machine JSON (Amazon States Language)**

Here’s a **simplified state machine definition**:

```json
{
  "Comment": "File Transfer Router",
  "StartAt": "Validate Input",
  "States": {
    "Validate Input": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_validate_input",
      "Next": "Route Based on Type",
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "Next": "Log Failure"
        }
      ]
    },
    "Route Based on Type": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.workflowId",
          "StringEquals": "copy-sftp-to-s3",
          "Next": "SFTP to S3 Lambda"
        },
        {
          "Variable": "$.workflowId",
          "StringEquals": "copy-s3-to-sftp",
          "Next": "S3 to SFTP Lambda"
        },
        {
          "Variable": "$.workflowId",
          "StringEquals": "copy-sftp-to-sftp",
          "Next": "SFTP to SFTP Lambda"
        },
        {
          "Variable": "$.workflowId",
          "StringEquals": "copy-s3-to-s3",
          "Next": "S3 to S3 Lambda"
        }
      ],
      "Default": "Log Failure"
    },
    "SFTP to S3 Lambda": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_sftp_to_s3",
      "Next": "Log Success"
    },
    "S3 to SFTP Lambda": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_s3_to_sftp",
      "Next": "Log Success"
    },
    "SFTP to SFTP Lambda": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_sftp_to_sftp",
      "Next": "Log Success"
    },
    "S3 to S3 Lambda": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_s3_to_s3",
      "Next": "Log Success"
    },
    "Log Success": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_log_success",
      "End": true
    },
    "Log Failure": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_log_failure",
      "End": true
    }
  }
}
```

---

### **Step 5.5: Deploy Step Function via Console or Terraform**

#### Option A: Console

* Go to AWS Step Functions → Create state machine
* Choose “Author with code snippets”
* Paste the JSON definition above
* Assign appropriate IAM Role

#### Option B: Terraform (Optional)

```hcl
resource "aws_sfn_state_machine" "file_transfer_router" {
  name     = "file-transfer-router"
  role_arn = aws_iam_role.step_function_role.arn

  definition = file("${path.module}/step_function_definition.json")
}
```

---

### **Step 5.6: Triggering the Step Function**

You can invoke the Step Function in two ways:

* **Manually from SQS consumer Lambda** (after it receives a message)
* Or automate using **EventBridge → Lambda → Step Function**

---

### **Step 5.7: Add Monitoring**

* Enable **logging** in Step Function for input/output
* Add **CloudWatch Alarms** on:

  * `ExecutionFailed`
  * `ExecutionTimedOut`
  * `LambdaFunctionErrors`

---

## ✅ Deliverables from Step 5

* ✔️ A visual routing engine for file workflows
* ✔️ Modular orchestration for multiple combinations
* ✔️ Lambda-based plug-and-play architecture
* ✔️ Easy extensibility with new workflows (just add new Choice branch)

Here is a complete list of **all the states** used in the Step Function **State Machine** for your AWS File Transfer Workflow:

---

### 🔄 **List of States (with Description)**

| **State Name**        | **Type** | **Purpose**                                                                |
| --------------------- | -------- | -------------------------------------------------------------------------- |
| `Validate Input`      | Task     | Validates required fields (e.g., bucket, key, workflowId) from SQS message |
| `Route Based on Type` | Choice   | Routes to the correct Lambda based on `workflowId`                         |
| `SFTP to S3 Lambda`   | Task     | Executes Python Lambda to copy from source SFTP → target S3 bucket         |
| `S3 to SFTP Lambda`   | Task     | Executes Python Lambda to copy from source S3 → target SFTP server         |
| `SFTP to SFTP Lambda` | Task     | Executes Python Lambda to copy from one SFTP server → another              |
| `S3 to S3 Lambda`     | Task     | Executes Python Lambda to copy between two S3 buckets                      |
| `Log Success`         | Task     | Logs success record in DynamoDB                                            |
| `Log Failure`         | Task     | Logs error and marks failure in DynamoDB                                   |

---

### 🧭 **Flow Summary**

```
Validate Input
   ↓
Route Based on Type
   ├─▶ SFTP to S3 Lambda
   ├─▶ S3 to SFTP Lambda
   ├─▶ SFTP to SFTP Lambda
   ├─▶ S3 to S3 Lambda
   ↓
Log Success / Log Failure
```

---

### 📌 Optional (Advanced Enhancements):

If you want to make it more robust later:

| **State Name**        | **Type** | **Purpose**                                                           |
| --------------------- | -------- | --------------------------------------------------------------------- |
| `Record Metrics`      | Task     | Push CloudWatch metrics per workflow                                  |
| `Send Notification`   | Task     | Optional SNS or EventBridge event after file transfer                 |
| `Check Retry Count`   | Choice   | Conditional routing for retry limit checks (via DynamoDB retry count) |
| `Manual Review Queue` | Pass     | Optional route to send failed records to human review                 |

Here is the **expanded list of all states** in your AWS Step Functions **State Machine**, now including the **Advanced Enhancements** for a production-grade file transfer workflow:

---

## ✅ **Full List of States (Basic + Advanced Enhancements)**

| **State Name**        | **Type** | **Purpose**                                                           |
| --------------------- | -------- | --------------------------------------------------------------------- |
| `Validate Input`      | Task     | Validate required fields in the incoming message (bucket, key, etc.)  |
| `Route Based on Type` | Choice   | Directs workflow to appropriate Lambda function based on `workflowId` |
| `SFTP to S3 Lambda`   | Task     | Python Lambda: Copy file from SFTP to S3                              |
| `S3 to SFTP Lambda`   | Task     | Python Lambda: Copy file from S3 to SFTP                              |
| `SFTP to SFTP Lambda` | Task     | Python Lambda: Copy file from SFTP to another SFTP                    |
| `S3 to S3 Lambda`     | Task     | Python Lambda: Copy file from S3 to another S3                        |
| `Log Success`         | Task     | Log successful transfer to DynamoDB and optionally to CloudWatch Logs |
| `Log Failure`         | Task     | Log failed transfer to DynamoDB and optionally send alert             |

---

## 🚀 **Advanced Enhancement States**

| **State Name**        | **Type**     | **Purpose**                                                            |
| --------------------- | ------------ | ---------------------------------------------------------------------- |
| `Record Metrics`      | Task         | Push CloudWatch custom metrics (duration, file size, customerId, etc.) |
| `Send Notification`   | Task         | Send SNS or EventBridge message on completion/failure                  |
| `Check Retry Count`   | Choice       | Check retry count from DynamoDB; reroute if threshold exceeded         |
| `Retry Transfer`      | Task         | Retry the Lambda transfer for transient issues                         |
| `Manual Review Queue` | Pass or Task | If retries fail, optionally route to DLQ or manual review queue        |
| `Update Retry Count`  | Task         | Increment retry counter in DynamoDB before retry                       |
| `Wait Before Retry`   | Wait         | Introduce a delay (e.g., 5 mins) before retrying to avoid throttling   |

---

## 🧭 **Workflow Example Including Enhancements**

```
[Validate Input]
      ↓
[Check Retry Count]
      ├──> [Retry Limit Exceeded?]
      │        ├── Yes → [Manual Review Queue] → [Log Failure]
      │        └── No  → [Update Retry Count] → [Wait Before Retry]
      ↓
[Route Based on Type]
      ↓
[Copy Lambda]
      ↓
[Log Success]
      ↓
[Record Metrics] 
      ↓
[Send Notification]
```

---

## 🔁 **Typical Retry Handling Branch**

```
[Check Retry Count]
      ↓
[Update Retry Count]
      ↓
[Wait Before Retry]
      ↓
[Route Based on Type] (Retry the copy operation)
```

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


Here’s a **detailed real-world example** of the enhanced AWS Step Functions workflow for a **file transfer use case**, incorporating your tech stack and advanced enhancements.

---

## ✅ **Scenario: Real-World File Transfer Workflow**

### 🎯 **Business Case**:

A **financial institution** receives daily transaction files from its **on-premises SFTP server** and an **external cloud partner’s S3 bucket**. These files need to be delivered securely to:

* A target **AWS-hosted SFTP server** (for downstream processing)
* A **centralized S3 bucket** for long-term archival

### 📁 File Types:

* `clientX_transactions_2025-06-28.csv`
* `clientX_balances_2025-06-28.csv`

---

## 🧱 **Architecture Stack**

| Component               | Technology                        |
| ----------------------- | --------------------------------- |
| Source                  | On-prem SFTP & External S3 Bucket |
| Transfer Mechanism      | AWS Transfer Family & EventBridge |
| Storage                 | S3 Landing Zone                   |
| Processing Orchestrator | AWS Step Functions                |
| Task Executors          | AWS Lambda (Python)               |
| Retry Tracking          | DynamoDB                          |
| Notifications           | SNS or EventBridge                |
| Monitoring              | CloudWatch Metrics & Logs         |

---

## 🚦 **Step-by-Step Execution Flow**

### 🔹 **Step 1: File Upload to S3**

* On-prem system pushes `clientX_transactions_2025-06-28.csv` to **AWS Transfer Family (SFTP)**.
* File lands in:
  `s3://sftp-landing-zone/from-sftp/clientX/clientX_transactions_2025-06-28.csv`

---

### 🔹 **Step 2: EventBridge Triggers on S3 Object Creation**

* EventBridge rule fires when an object is created in the prefix `from-sftp/clientX/`.
* Target is an **SQS queue** (`file-transfer-queue`).
* Message Body:

```json
{
  "bucket": "sftp-landing-zone",
  "key": "from-sftp/clientX/clientX_transactions_2025-06-28.csv",
  "sourceType": "SFTP",
  "target": "s3://clientX-final-destination",
  "targetType": "S3",
  "workflowId": "copy-sftp-to-s3",
  "customerId": "clientX"
}
```

---

### 🔹 **Step 3: Lambda Trigger Reads SQS and Starts Step Function**

Lambda `trigger_state_machine.py` invokes the Step Function with the message as input.

---

### 🔹 **Step 4: Step Function Workflow Execution**

#### 🟩 `Validate Input`

* Validates `bucket`, `key`, `workflowId`, `customerId`.

#### 🟩 `Check Retry Count`

* Queries `DynamoDB` to get retry count for the current file key.

#### 🟩 `Update Retry Count`

* If retryCount < 3, increment in DynamoDB.

#### 🟨 `Wait Before Retry`

* Waits for 5 minutes before attempting again (backoff logic).

#### 🟩 `Route Based on Type`

* Routes to `lambda_sftp_to_s3.py`.

#### 🟩 `lambda_sftp_to_s3.py` runs:

* Downloads the file from `sftp-landing-zone/from-sftp/clientX/...`.
* Uploads it to:
  `s3://clientX-final-destination/clientX_transactions_2025-06-28.csv`

---

### 🔹 **Step 5: Post-Transfer Actions**

#### 🟩 `Log Success`

* Writes to DynamoDB:

```json
{
  "workflowId": "copy-sftp-to-s3",
  "timestamp": "2025-06-28T22:00:00Z",
  "fileKey": "clientX_transactions_2025-06-28.csv",
  "customerId": "clientX",
  "status": "SUCCESS"
}
```

#### 🟩 `Record Metrics`

* Publishes CloudWatch custom metric:
  `MetricName: FileTransferSuccess`, `Dimensions: CustomerId=clientX`

#### 🟩 `Send Notification`

* Publishes SNS notification:

> ✅ File `clientX_transactions_2025-06-28.csv` successfully transferred for customer *clientX*.

---

## ❌ If Something Fails...

If the Lambda fails (e.g., target S3 permissions misconfigured):

* Step Function goes to:

  * `Update Retry Count`
  * `Wait Before Retry`
  * Retries up to 3 times
* If still failing:

  * Routes to `Manual Review Queue` (or DLQ)
  * Sends alert via SNS
  * Marks status as `"FAILED"` in DynamoDB

---

## 📊 Monitoring

* CloudWatch Dashboard shows:

  * Number of successful/failed transfers per day per client
  * Lambda duration, errors
* Alarms notify if:

  * Transfer failures > threshold
  * Step Function execution time exceeds SLA

---

## 🧪 Test Scenario

1. Drop a file in SFTP: ✅
2. Step Function triggers within seconds via EventBridge → SQS → Lambda → Step Function.
3. File arrives in target S3 bucket.
4. Email/SMS sent.
5. Entry logged in DynamoDB.

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


Perfect — you **do not want a Lambda to act as a middleman**, and instead want the **Step Function to be directly triggered by an SQS message**. This is supported via **Step Functions' `SQS → Express Workflow` integration**.

---

## ✅ Updated Architecture: Step Function Triggered Directly from SQS

```
[S3 or SFTP]
     │
     ▼
[EventBridge]
     │
     ▼
[SQS Queue: file-transfer-queue]
     │
     ▼
[Step Function (Express)]
   - Validate
   - Route
   - Copy
   - Log
   - Notify
```

---

## 🧭 Step-by-Step: Trigger Step Function from SQS

---

### **Step 1: Set Up an Express Step Function**

Only **Express Workflows** support **event sources** like SQS.

* Go to AWS → Step Functions → **Create state machine**
* Choose **Express** type
* Define your workflow (states like `Validate Input`, `Route Based on Type`, etc.)

---

### **Step 2: Create or Use SQS Queue**

If not already created:

```bash
aws sqs create-queue --queue-name file-transfer-queue
```

---

### **Step 3: Configure Event Source Mapping (SQS → Step Function)**

Use the console or the CLI to **attach SQS as a trigger** to your Express Step Function.

#### ✅ Using AWS Console:

1. Go to your Step Function
2. Click **"Triggers"** tab
3. Select **"SQS"**
4. Choose your queue: `file-transfer-queue`
5. Set **Batch size** (e.g., 1 or 10)
6. Confirm IAM permissions:

   * Step Function role must have `sqs:ReceiveMessage`, `sqs:DeleteMessage`

#### ✅ IAM Policy Required on Step Function Role:

```json
{
  "Effect": "Allow",
  "Action": [
    "sqs:ReceiveMessage",
    "sqs:DeleteMessage",
    "sqs:GetQueueAttributes",
    "sqs:GetQueueUrl"
  ],
  "Resource": "arn:aws:sqs:<region>:<account-id>:file-transfer-queue"
}
```

---

### **Step 4: Format of SQS Message (Payload)**

Your EventBridge should send the following structure to SQS, which will be directly passed into Step Function:

```json
{
  "bucket": "sftp-landing-zone",
  "key": "from-sftp/clientX/file.csv",
  "workflowId": "copy-sftp-to-s3",
  "customerId": "clientX",
  "sourceType": "SFTP",
  "targetType": "S3",
  "target": "s3://clientX-final"
}
```

The **entire SQS message body** becomes the Step Function input.

---

### **Step 5: Step Function JSON Definition Example (Simplified)**

```json
{
  "StartAt": "Validate Input",
  "States": {
    "Validate Input": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:region:acct:function:lambda_validate_input",
      "Next": "Route Based on Type"
    },
    "Route Based on Type": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.workflowId",
          "StringEquals": "copy-sftp-to-s3",
          "Next": "SFTP to S3 Lambda"
        }
        // more choices...
      ],
      "Default": "Log Failure"
    },
    "SFTP to S3 Lambda": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:region:acct:function:lambda_sftp_to_s3",
      "Next": "Log Success"
    },
    "Log Success": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:region:acct:function:lambda_log_success",
      "End": true
    },
    "Log Failure": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:region:acct:function:lambda_log_failure",
      "End": true
    }
  }
}
```

---

### 🧪 Bonus: Retry & DLQ

* You can define **max retry attempts** in the trigger settings
* Optionally configure a **Dead Letter Queue** if messages fail to process after retries

---

## ✅ Benefits of SQS → Step Function (No Lambda Middleman)

| Feature            | Value                                      |
| ------------------ | ------------------------------------------ |
| Lower cost         | No always-running Lambda for triggering    |
| Better throughput  | Supports batching and concurrency natively |
| Simplified flow    | EventBridge → SQS → Step Function directly |
| Native integration | Managed by AWS with retry and batching     |

+++++++++++++++++++++++++++++++++++++++++++++++++++


Great! Let’s now walk through the **entire AWS File Transfer workflow**, **step-by-step**, using a **real-world example** — with **no Lambda trigger**, and instead **SQS triggers the Step Function directly**.

---

## ✅ Real-World Example: Bank File Transfer Workflow

### 🏦 Scenario:

A **bank's internal reconciliation team** sends transaction files from their **on-premises SFTP system** every evening. These must be:

1. Moved securely to a **central S3 bucket** for archival.
2. Also uploaded to a **partner-access SFTP server** hosted in AWS Transfer Family.

---

## 🔧 Tech Stack Used

| Purpose                      | Service Used                 |
| ---------------------------- | ---------------------------- |
| Secure File Upload (On-prem) | AWS Transfer Family (SFTP)   |
| Landing Zone                 | Amazon S3                    |
| Event Notification           | Amazon EventBridge           |
| Triggering Workflow          | Amazon SQS                   |
| Orchestration                | AWS Step Functions (Express) |
| Task Execution               | AWS Lambda (Python)          |
| Status Tracking              | DynamoDB                     |
| Alerting                     | SNS or EventBridge           |

---

## 🧭 Step-by-Step Workflow (with Real Example)

---

### **Step 1: File Uploaded to AWS Transfer Family (SFTP)**

* The on-prem batch job sends a file:

  ```
  clientX_transactions_2025-06-28.csv
  ```
* Transfer Family SFTP drops it to:

  ```
  s3://sftp-landing-zone/from-sftp/clientX/clientX_transactions_2025-06-28.csv
  ```

---

### **Step 2: EventBridge Rule Triggers on S3 Upload**

* EventBridge rule pattern:

  ```json
  {
    "source": ["aws.s3"],
    "detail-type": ["Object Created"],
    "detail": {
      "bucket": { "name": ["sftp-landing-zone"] },
      "object": {
        "key": [{ "prefix": "from-sftp/clientX/" }]
      }
    }
  }
  ```

* The EventBridge rule sends a message to `file-transfer-queue` (SQS):

  ```json
  {
    "bucket": "sftp-landing-zone",
    "key": "from-sftp/clientX/clientX_transactions_2025-06-28.csv",
    "workflowId": "copy-sftp-to-s3-and-sftp",
    "customerId": "clientX",
    "sourceType": "SFTP",
    "targetType": "S3_SFTP",
    "targets": {
      "s3": "s3://bank-archive-bucket/clientX/",
      "sftp": "sftp://aws-transfer-partner-server/clientX/"
    }
  }
  ```

---

### **Step 3: SQS Message Triggers Step Function Directly**

* **No Lambda** needed here.
* Step Function is **Express** type.
* It’s configured with **SQS as a native trigger**.

---

### **Step 4: Step Function Executes**

Let’s walk through each **state in the workflow**:

---

#### 🟢 **State: Validate Input**

Lambda `lambda_validate_input.py` ensures:

* `bucket`, `key`, and `workflowId` are present.
* File name format is correct (using regex for `clientX_transactions_YYYY-MM-DD.csv`).
* Result: PASS ✅ → move to next step.

---

#### 🟢 **State: Check Retry Count (DynamoDB)**

Checks in `FileTransferStatus` table:

```dynamodb
Key: clientX_transactions_2025-06-28.csv
Value: {
  retryCount: 0,
  status: "PENDING"
}
```

If `retryCount` < 3 → continue.

---

#### 🟡 **State: Update Retry Count**

If this is a retry attempt, increment `retryCount` in DynamoDB.

---

#### ⏱️ **State: Wait Before Retry (Optional)**

Waits for 300 seconds to avoid repeated rapid failure in case of transient issues.

---

#### 🧠 **State: Route Based on Type**

Checks `workflowId: copy-sftp-to-s3-and-sftp`

Routes to parallel execution of:

* `lambda_sftp_to_s3.py`
* `lambda_sftp_to_sftp.py`

---

#### 🔁 **State: lambda\_sftp\_to\_s3.py**

Python Lambda does:

1. Uses `boto3` to copy file from:

   * `s3://sftp-landing-zone/from-sftp/clientX/...`
2. To target:

   * `s3://bank-archive-bucket/clientX/clientX_transactions_2025-06-28.csv`

---

#### 🔁 **State: lambda\_sftp\_to\_sftp.py**

1. Reads file from source S3 (Transfer Family backend)
2. Uploads to **target SFTP server** (Transfer Family target backend)

   * Backend is a **different S3 bucket**, e.g. `s3://partner-sftp-backend/clientX/`
3. Can use `start-file-transfer` API or simply copy to S3 backend folder

---

#### ✅ **State: Log Success**

Writes to DynamoDB:

```json
{
  "fileKey": "clientX_transactions_2025-06-28.csv",
  "customerId": "clientX",
  "status": "SUCCESS",
  "timestamp": "2025-06-28T22:01:34Z"
}
```

---

#### 📊 **State: Record Metrics**

Publishes to CloudWatch:

```json
{
  "MetricName": "FileTransferSuccess",
  "Dimensions": {
    "Customer": "clientX",
    "WorkflowId": "copy-sftp-to-s3-and-sftp"
  },
  "Value": 1
}
```

---

#### 📣 **State: Send Notification**

SNS Topic sends email or webhook:

> ✅ File `clientX_transactions_2025-06-28.csv` successfully processed for clientX.

---

### ❌ If Something Fails:

* Step Function automatically retries Lambda up to `maxAttempts`.
* If retries exhausted:

  * State `Log Failure` writes failure status to DynamoDB
  * Optional: send to `manual-review-queue`
  * Send alert via SNS:

    > ❌ Transfer failed for file: clientX\_transactions\_2025-06-28.csv after 3 attempts

---

## ✅ Final Result

| Action                        | Outcome                                |
| ----------------------------- | -------------------------------------- |
| File from SFTP landed in S3   | ✅                                      |
| Transferred to S3 archive     | ✅                                      |
| Copied to partner SFTP server | ✅                                      |
| Logged in DynamoDB            | ✅                                      |
| Notified bank team            | ✅ (via SNS/Email)                      |
| Retry/Failure monitored       | ✅ (CloudWatch + Step Function retries) |

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


Here is the **complete Step Function ASL (Amazon States Language) JSON definition** for your **real-world example**:

### ✅ Use Case:

> Copy a file uploaded to SFTP → S3 (landing zone) to both:
>
> * Target S3 archive bucket
> * AWS-hosted SFTP server (with S3 backend)

---

## 🧾 Step Function Name: `copy-sftp-to-s3-and-sftp-workflow`

### 🔁 Type: **Express Workflow**

```json
{
  "Comment": "Copy file from SFTP to S3 Archive and SFTP Partner Server",
  "StartAt": "Validate Input",
  "States": {
    "Validate Input": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_validate_input",
      "Next": "Check Retry Count",
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "Next": "Log Failure"
        }
      ]
    },
    "Check Retry Count": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_check_retry_count",
      "Next": "Should Retry?"
    },
    "Should Retry?": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.retryCount",
          "NumericLessThan": 3,
          "Next": "Update Retry Count"
        }
      ],
      "Default": "Manual Review Queue"
    },
    "Update Retry Count": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_update_retry_count",
      "Next": "Wait Before Retry"
    },
    "Wait Before Retry": {
      "Type": "Wait",
      "Seconds": 300,
      "Next": "Route Workflow"
    },
    "Manual Review Queue": {
      "Type": "Pass",
      "Result": "Exceeded retry limit. Manual intervention required.",
      "Next": "Log Failure"
    },
    "Route Workflow": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.workflowId",
          "StringEquals": "copy-sftp-to-s3-and-sftp",
          "Next": "Copy in Parallel"
        }
      ],
      "Default": "Log Failure"
    },
    "Copy in Parallel": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "Copy to S3 Archive",
          "States": {
            "Copy to S3 Archive": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_sftp_to_s3",
              "End": true
            }
          }
        },
        {
          "StartAt": "Copy to SFTP Partner",
          "States": {
            "Copy to SFTP Partner": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_sftp_to_sftp",
              "End": true
            }
          }
        }
      ],
      "Next": "Log Success",
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "Next": "Log Failure"
        }
      ]
    },
    "Log Success": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_log_success",
      "Next": "Record Metrics"
    },
    "Record Metrics": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_record_metrics",
      "Next": "Send Notification"
    },
    "Send Notification": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_send_notification",
      "End": true
    },
    "Log Failure": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:lambda_log_failure",
      "End": true
    }
  }
}
```

---

### 📝 Replace Placeholders:

| Placeholder  | Replace with...                                 |
| ------------ | ----------------------------------------------- |
| `REGION`     | e.g., `us-west-2`                               |
| `ACCOUNT_ID` | Your AWS Account ID                             |
| Lambda ARNs  | Ensure each function exists in your environment |

---

## ✅ Key Capabilities

| Capability              | Built-in via states                                 |
| ----------------------- | --------------------------------------------------- |
| Retry logic             | `Check Retry Count`, `Update Retry Count`           |
| Wait/backoff            | `Wait Before Retry`                                 |
| Parallel file copy      | `Copy to S3` and `Copy to SFTP` in `Parallel` block |
| Failure logging         | `Log Failure`                                       |
| Monitoring + metrics    | `Record Metrics`                                    |
| Notification on success | `Send Notification`                                 |
| Manual review path      | `Manual Review Queue`                               |

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



Perfect. Let's now focus on the **DynamoDB table design** for your AWS File Transfer architecture. This table (or tables) will be used to:

* Track file transfer statuses
* Log retry counts
* Store metadata about file copies
* Enable status queries and reporting

---

## ✅ **Goals for DynamoDB in this Architecture**

| **Use Case**                                | **Supported By**            |
| ------------------------------------------- | --------------------------- |
| Track success/failure of file transfers     | `FileTransferStatus` table  |
| Support retry logic                         | Retry counter in DynamoDB   |
| Enable querying by file, customer, date     | Partition/sort key modeling |
| View all files transferred per customer/day | GSI or composite key        |
| Lookup latest status for a file             | PK = fileId or composite ID |

---

## 🧱 DynamoDB Table Design

### 📘 Table 1: `FileTransferStatus`

| Field Name     | Type     | Description                                   |
| -------------- | -------- | --------------------------------------------- |
| `PK`           | `STRING` | Partition Key: `FILE#<customerId>#<fileName>` |
| `SK`           | `STRING` | Sort Key: `TS#<ISO-Timestamp>`                |
| `fileName`     | `STRING` | Just the filename                             |
| `customerId`   | `STRING` | ID of the customer/client                     |
| `sourceBucket` | `STRING` | Source S3 bucket or SFTP path                 |
| `target`       | `MAP`    | Includes S3/SFTP targets                      |
| `workflowId`   | `STRING` | Workflow pattern ID (e.g., `copy-sftp-to-s3`) |
| `status`       | `STRING` | `PENDING`, `IN_PROGRESS`, `SUCCESS`, `FAILED` |
| `retryCount`   | `NUMBER` | Count of retries                              |
| `errorMessage` | `STRING` | Last failure reason                           |
| `timestamp`    | `STRING` | ISO timestamp                                 |
| `metadata`     | `MAP`    | Any additional metadata                       |

#### 🔑 Example Keys:

* `PK`: `FILE#clientX#clientX_transactions_2025-06-28.csv`
* `SK`: `TS#2025-06-28T22:00:00Z`

#### ✅ Benefits:

* Query by file (exact match)
* Query all transfers for a client+file
* Easy to support version history (sorted by timestamp)

---

### 📘 Table 2: (Optional) `CustomerFileIndex` — for reporting

| Field Name      | Type     | Description                    |
| --------------- | -------- | ------------------------------ |
| `PK`            | `STRING` | `CUSTOMER#<customerId>`        |
| `SK`            | `STRING` | `DATE#<YYYY-MM-DD>#<fileName>` |
| `fileId`        | `STRING` | Can match PK of main table     |
| `status`        | `STRING` | Final transfer status          |
| `workflowId`    | `STRING` | Workflow pattern               |
| `targetSummary` | `STRING` | S3 / SFTP copy result          |
| `retryCount`    | `NUMBER` | Retry count                    |

#### 🔍 Usage:

* Get all files transferred by a client on a given day
* Paginate file history for reporting

---

## 🔄 Common Access Patterns & Queries

| **Query**                                                  | **How it's Handled**                                  |
| ---------------------------------------------------------- | ----------------------------------------------------- |
| Has file `F1` for `clientX` been successfully transferred? | GetItem with `PK = FILE#clientX#F1`, `SK` = latest TS |
| What was the last status of a given file?                  | Sort by TS descending, get latest                     |
| Show all files transferred by `clientY` on 2025-06-28      | Use `CustomerFileIndex` table or GSI                  |
| How many retries for `clientZ_file123.csv`?                | Read `retryCount` in `FileTransferStatus`             |
| Show all failed transfers for a customer                   | Use filter expressions or export with Athena          |

---

## ✏️ Sample Record (FileTransferStatus)

```json
{
  "PK": "FILE#clientX#clientX_transactions_2025-06-28.csv",
  "SK": "TS#2025-06-28T22:01:34Z",
  "fileName": "clientX_transactions_2025-06-28.csv",
  "customerId": "clientX",
  "sourceBucket": "sftp-landing-zone",
  "target": {
    "s3": "s3://bank-archive-bucket/clientX/",
    "sftp": "sftp://aws-transfer-partner-server/clientX/"
  },
  "workflowId": "copy-sftp-to-s3-and-sftp",
  "status": "SUCCESS",
  "retryCount": 1,
  "errorMessage": null,
  "timestamp": "2025-06-28T22:01:34Z",
  "metadata": {
    "fileSizeBytes": 5234412,
    "sha256": "abc123...",
    "initiatedBy": "EventBridge"
  }
}
```

---

## 🔐 IAM Permissions for Lambda Accessing DynamoDB

```json
{
  "Effect": "Allow",
  "Action": [
    "dynamodb:GetItem",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem",
    "dynamodb:Query"
  ],
  "Resource": [
    "arn:aws:dynamodb:REGION:ACCOUNT_ID:table/FileTransferStatus",
    "arn:aws:dynamodb:REGION:ACCOUNT_ID:table/CustomerFileIndex"
  ]
}
```

---

## 📈 Optional: Query with Athena

* Use **S3 export of DynamoDB** for Athena queries
* Great for dashboards/reporting in Amazon QuickSight

Here’s a list of **all the DynamoDB tables** you should consider for your **AWS File Transfer Architecture**, based on the needs of tracking, retry, logging, customer access, and auditability:

---

## ✅ **Primary DynamoDB Tables**

| **Table Name**            | **Purpose**                                                                 |
| ------------------------- | --------------------------------------------------------------------------- |
| `FileTransferStatus`      | Tracks detailed status of each file transfer, retry counts, metadata        |
| `CustomerFileIndex`       | Enables querying file transfers per customer and date (for reporting & UI)  |
| `WorkflowDefinition`      | Stores JSON-based workflow definitions for self-serve onboarding or routing |
| `FileTransferAuditLog`    | Logs every file transfer attempt (append-only audit history)                |
| `TransferFailureQueue`    | Holds records of permanently failed transfers (beyond retry limit)          |
| `TransferNotificationLog` | Logs notifications (SNS/Webhooks) sent for file events                      |

---

## 📘 **Details for Each Table**

---

### 1. **`FileTransferStatus`** (Core Tracking Table)

| Key Schema         | Value                          |
| ------------------ | ------------------------------ |
| Partition Key (PK) | `FILE#<customerId>#<fileName>` |
| Sort Key (SK)      | `TS#<ISO timestamp>`           |

🔹 **Purpose**:
Track the current and past status of each file, retry count, and workflow used.

---

### 2. **`CustomerFileIndex`** (Secondary Index Table for UI/Reports)

| Key Schema         | Value                          |
| ------------------ | ------------------------------ |
| Partition Key (PK) | `CUSTOMER#<customerId>`        |
| Sort Key (SK)      | `DATE#<yyyy-mm-dd>#<fileName>` |

🔹 **Purpose**:
Quickly list files processed per day per customer (used in dashboards, APIs, portals).

---

### 3. **`WorkflowDefinition`** (For Self-Serve JSON-Based Routing)

| Key Schema         | Value                   |
| ------------------ | ----------------------- |
| Partition Key (PK) | `WORKFLOW#<workflowId>` |

🔹 **Purpose**:
Store routing logic, targets, validation rules for each `workflowId`.

Example entry:

```json
{
  "PK": "WORKFLOW#copy-sftp-to-s3",
  "source": "SFTP",
  "target": "S3",
  "validationRegex": ".*\\.csv",
  "defaultRetry": 3
}
```

---

### 4. **`FileTransferAuditLog`** (Append-Only History Log)

| Key Schema         | Value                |
| ------------------ | -------------------- |
| Partition Key (PK) | `FILE#<fileName>`    |
| Sort Key (SK)      | `TS#<ISO timestamp>` |

🔹 **Purpose**:
Full history of every event (validation, copy start, copy end, retry, error) for auditing and compliance.

---

### 5. **`TransferFailureQueue`** (Dead Letter Tracker)

| Key Schema         | Value                                             |
| ------------------ | ------------------------------------------------- |
| Partition Key (PK) | `FAILURE#<fileName>`                              |
| Attributes         | `reason`, `lastStatus`, `customerId`, `timestamp` |

🔹 **Purpose**:
Store permanently failed transfers for manual reprocessing or exception workflow.

---

### 6. **`TransferNotificationLog`** (Notification Tracker)

| Key Schema         | Value                |
| ------------------ | -------------------- |
| Partition Key (PK) | `NOTIFY#<fileName>`  |
| Sort Key (SK)      | `TS#<ISO timestamp>` |

🔹 **Purpose**:
Track what notifications (email, webhook, SNS) were sent and their success/failure.

---

## 🧠 Optional: Global Secondary Indexes (GSI)

You can add GSIs for advanced queries:

| **GSI Name** | **Partition Key** | **Sort Key** | **Purpose**                        |
| ------------ | ----------------- | ------------ | ---------------------------------- |
| `GSI1`       | `customerId`      | `status`     | List failed transfers per customer |
| `GSI2`       | `workflowId`      | `timestamp`  | Show transfer history by workflow  |

![image](https://github.com/user-attachments/assets/b54c2d95-2382-4ff4-b1ae-6e41709b8fb2)



Here's a detailed breakdown of the **`FileTransferStatus`** DynamoDB table, which serves as the **central tracking and state management** table in your AWS File Transfer architecture.

---

## ✅ **Table: `FileTransferStatus`**

### 📌 **Primary Purpose**

Track the **state, retry count, and metadata** of every file processed through your transfer workflows (SFTP → S3, S3 → SFTP, etc.).

---

## 🔑 **Key Schema**

| Key Type      | Key Name                 | Format Example                                     |
| ------------- | ------------------------ | -------------------------------------------------- |
| Partition Key | `PK` (File Identifier)   | `FILE#clientX#clientX_transactions_2025-06-28.csv` |
| Sort Key      | `SK` (Version/Timestamp) | `TS#2025-06-28T22:01:34Z`                          |

This schema allows **versioning** of status entries for the same file (by timestamp).

---

## 📋 **Attributes**

| Attribute      | Type   | Description                                                 |
| -------------- | ------ | ----------------------------------------------------------- |
| `fileName`     | String | Original file name (`clientX_transactions_2025-06-28.csv`)  |
| `customerId`   | String | ID or name of the client/customer                           |
| `sourceBucket` | String | S3 bucket or identifier of the source system                |
| `target`       | Map    | Map of target types and locations (e.g., S3 URI, SFTP path) |
| `workflowId`   | String | ID of the workflow used (e.g., `copy-sftp-to-s3`)           |
| `status`       | String | `PENDING`, `IN_PROGRESS`, `SUCCESS`, `FAILED`               |
| `retryCount`   | Number | Number of retries attempted                                 |
| `errorMessage` | String | Last error message encountered (nullable)                   |
| `timestamp`    | String | ISO timestamp of current entry                              |
| `metadata`     | Map    | Additional info like file size, hash, triggeredBy, etc.     |

---

## 📘 **Sample Item**

```json
{
  "PK": "FILE#clientX#clientX_transactions_2025-06-28.csv",
  "SK": "TS#2025-06-28T22:01:34Z",
  "fileName": "clientX_transactions_2025-06-28.csv",
  "customerId": "clientX",
  "sourceBucket": "sftp-landing-zone",
  "target": {
    "s3": "s3://bank-archive-bucket/clientX/",
    "sftp": "sftp://aws-transfer-partner-server/clientX/"
  },
  "workflowId": "copy-sftp-to-s3-and-sftp",
  "status": "SUCCESS",
  "retryCount": 1,
  "errorMessage": null,
  "timestamp": "2025-06-28T22:01:34Z",
  "metadata": {
    "fileSizeBytes": 5234412,
    "sha256": "abc123...",
    "triggeredBy": "EventBridge"
  }
}
```

---

## 🔍 **Typical Access Patterns**

| Use Case                                       | Operation           | Query Example                                           |
| ---------------------------------------------- | ------------------- | ------------------------------------------------------- |
| Get latest status for a specific file          | `Query` + Desc sort | PK = `FILE#clientX#clientX_transactions_2025-06-28.csv` |
| All versions/history of a file transfer        | `Query`             | Same as above, sort ascending                           |
| Lookup by customer or date                     | Use GSI (optional)  | GSI1: `customerId`, GSI2: `workflowId` + timestamp      |
| Identify files with failures or pending status | `Scan` or export    | Filter by `status != SUCCESS`                           |

---

## 🚦 Best Practices

* **Enable Time-to-Live (TTL)** for old items if not needed for audit
* Use **write-once, append-only model** if compliance history is needed
* Add **DynamoDB Streams** if you want to trigger alerts on `FAILED` status

Here’s a **real-world example** of a fully populated `FileTransferStatus` item, as it would appear in a **DynamoDB record** during an actual file transfer scenario within your AWS file transfer architecture.

---

## 🏦 **Scenario**:

**Bank of Pacific** is a financial services client (`customerId: bankpacific`) that uploads a nightly transaction batch via AWS Transfer Family (SFTP). A file named:

```
bankpacific_transactions_2025-06-28.csv
```

is uploaded to:

```
s3://sftp-landing-zone/from-sftp/bankpacific/bankpacific_transactions_2025-06-28.csv
```

The workflow is configured to:

1. Move the file to a **secure S3 archive** bucket.
2. Copy the file to a **partner-facing AWS SFTP server**.

---

## 📘 **FileTransferStatus – Sample DynamoDB Record**

```json
{
  "PK": "FILE#bankpacific#bankpacific_transactions_2025-06-28.csv",
  "SK": "TS#2025-06-28T22:01:34Z",
  "fileName": "bankpacific_transactions_2025-06-28.csv",
  "customerId": "bankpacific",
  "sourceBucket": "sftp-landing-zone",
  "target": {
    "s3": "s3://archive-bucket-secure/bankpacific/2025-06/",
    "sftp": "sftp://aws-transfer/bankpacific/partner-dropzone/"
  },
  "workflowId": "copy-sftp-to-s3-and-sftp",
  "status": "SUCCESS",
  "retryCount": 1,
  "errorMessage": null,
  "timestamp": "2025-06-28T22:01:34Z",
  "metadata": {
    "fileSizeBytes": 4352176,
    "sha256": "b90c8de9f47ad86f408c2a47dcd2e77b7d11629ea5f9c35c76524e0b2c0b6b6e",
    "fileType": "csv",
    "uploadMethod": "AWS Transfer Family",
    "initiatedBy": "EventBridge-S3",
    "region": "us-west-2"
  }
}
```

---

## 🔍 **Field Breakdown**

| Field          | Description                                                          |
| -------------- | -------------------------------------------------------------------- |
| `PK` / `SK`    | Composite key: enables tracking & versioning per file                |
| `fileName`     | Name of the file uploaded by client                                  |
| `customerId`   | Useful for partitioning and filtering                                |
| `sourceBucket` | S3 bucket where file landed via SFTP                                 |
| `target`       | Map of S3 and SFTP destination locations                             |
| `workflowId`   | Defines processing route (used in Step Function routing)             |
| `status`       | Final status of the file (`SUCCESS`, `FAILED`, `IN_PROGRESS`, etc.)  |
| `retryCount`   | Number of attempts made by Step Function before success              |
| `errorMessage` | If any error occurred during transfer, it's logged here              |
| `timestamp`    | ISO timestamp (used in SK and GSI)                                   |
| `metadata`     | Rich info: hash for integrity, size for billing, source for auditing |

---

## 🔄 **Example Lifecycle for This File**

| Event           | Description                                       |
| --------------- | ------------------------------------------------- |
| ✅ Upload        | File uploaded via AWS SFTP to S3 landing zone     |
| 🔁 Retry        | First transfer to S3 archive failed; retried once |
| ✅ Success       | Both S3 and SFTP transfers succeeded              |
| 🧾 Logged       | DynamoDB record created with final state and hash |
| 🔔 Notification | Notification sent via SNS to audit team           |

---

## 📊 Example Query

To query all records for this file:

```bash
# Using AWS SDK or CLI:
PK = "FILE#bankpacific#bankpacific_transactions_2025-06-28.csv"
Sort Descending on SK to get latest entry
```

Certainly! Let’s break down the **Partition Key (PK)** design used in your DynamoDB `FileTransferStatus` table, specifically:

---

## 🧩 **PK = "FILE#bankpacific#bankpacific\_transactions\_2025-06-28.csv"**

This is a **composite string key** designed for precise and efficient access to each unique file uploaded by a customer.

---

### ✅ **Why use a composite PK?**

DynamoDB requires a **Partition Key (and optionally a Sort Key)** to uniquely identify and efficiently retrieve items. By combining **file metadata (customer + filename)** into a single structured string, we gain:

* Fast direct lookup
* Namespace separation by customer
* Natural file-level grouping

---

## 🔍 **Detailed Breakdown of the PK**

```
"FILE#bankpacific#bankpacific_transactions_2025-06-28.csv"
```

| Segment                                   | Purpose                                                      |
| ----------------------------------------- | ------------------------------------------------------------ |
| `FILE`                                    | A static prefix to **namespace the item type**               |
| `bankpacific`                             | The **customer ID or name** — enables partitioning by client |
| `bankpacific_transactions_2025-06-28.csv` | The **full filename** — uniquely identifies the file         |

> 💡 Think of this as saying:
> “This item is a FILE belonging to `bankpacific` with the name `bankpacific_transactions_2025-06-28.csv`.”

---

### 🧠 **Why prefix with `FILE#`?**

Using static prefixes like `FILE#` is a **best practice in DynamoDB modeling** when you store multiple types of items (e.g., workflows, files, audit logs) in the same table or to **future-proof** the design.

It allows queries like:

```bash
PK begins_with "FILE#bankpacific"
```

To get **all files uploaded by a specific client** — very useful for admin dashboards or reporting.

---

### 🔄 **How it Works in Practice**

Let’s say you want to store transfer status history for this file:

1. **First upload (initial status)**

   ```text
   PK = "FILE#bankpacific#bankpacific_transactions_2025-06-28.csv"
   SK = "TS#2025-06-28T21:00:00Z"
   status = "PENDING"
   ```

2. **After processing started**

   ```text
   SK = "TS#2025-06-28T21:01:00Z"
   status = "IN_PROGRESS"
   ```

3. **After successful transfer**

   ```text
   SK = "TS#2025-06-28T21:03:12Z"
   status = "SUCCESS"
   ```

> All these records share the **same PK** but have different **SKs (timestamps)**.
> This enables **version history**, and lets you always query for the latest status.

---

## 📈 **Query Use Cases Enabled by this PK Design**

| Query Type                          | How it's done with PK                     |
| ----------------------------------- | ----------------------------------------- |
| Get status of a specific file       | GetItem using full PK                     |
| List all files for a customer       | `begins_with(PK, 'FILE#bankpacific')`     |
| Get all status changes for a file   | Query PK, sort by SK                      |
| Aggregate transfer count per client | Scan by `FILE#client` prefix (or use GSI) |

---

## 🛠️ **Example Boto3 Query (Python)**

```python
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FileTransferStatus')

response = table.query(
    KeyConditionExpression=boto3.dynamodb.conditions.Key('PK').eq('FILE#bankpacific#bankpacific_transactions_2025-06-28.csv'),
    ScanIndexForward=False,  # Get latest status first
    Limit=1
)

item = response['Items'][0]
print("Latest status:", item['status'])
```

---

## ✅ Summary

| Feature             | Benefit                                                               |
| ------------------- | --------------------------------------------------------------------- |
| Composite PK        | Enables exact and fuzzy matching, partitioning by customer            |
| Timestamped SK      | Supports full history, retries, and time-series queries               |
| Prefixed Key Format | Scalable, supports multiple entity types in same table (future-proof) |



Great! Let’s now deep-dive into the **`CustomerFileIndex`** DynamoDB table — which complements your `FileTransferStatus` table by enabling **efficient querying of files by customer and date**, especially for UI dashboards and reporting use cases.

---

## ✅ **Table: `CustomerFileIndex`**

### 📌 Purpose:

To enable fast, filterable access to **all files uploaded or processed by a customer**, organized by **date and file name** — ideal for:

* UI portals (file status per client/day)
* Reporting dashboards (QuickSight, Athena)
* Admin audit tools

---

## 🧩 **Key Schema**

| Key Type      | Key Name | Example Value                                             |
| ------------- | -------- | --------------------------------------------------------- |
| Partition Key | `PK`     | `CUSTOMER#bankpacific`                                    |
| Sort Key      | `SK`     | `DATE#2025-06-28#bankpacific_transactions_2025-06-28.csv` |

This lets you query:

```sql
PK = "CUSTOMER#bankpacific"
AND SK begins_with "DATE#2025-06-28"
```

To get all files for that customer **on a given date**.

---

## 📋 **Attributes**

| Attribute       | Type       | Description                                                       |
| --------------- | ---------- | ----------------------------------------------------------------- |
| `fileId`        | String     | Matches `PK` of `FileTransferStatus` table                        |
| `fileName`      | String     | The filename                                                      |
| `customerId`    | String     | Customer identifier                                               |
| `status`        | String     | Final transfer status: `SUCCESS`, `FAILED`, etc.                  |
| `workflowId`    | String     | Transfer route ID (`copy-sftp-to-s3`, etc.)                       |
| `targetSummary` | Map/String | Summary of where the file was delivered (S3 path, SFTP URL, etc.) |
| `retryCount`    | Number     | Final retry count before success/failure                          |
| `timestamp`     | String     | Time of latest update (ISO format)                                |
| `errorMessage`  | String     | If failed, reason for failure                                     |

---

## 🧾 **Sample Item**

```json
{
  "PK": "CUSTOMER#bankpacific",
  "SK": "DATE#2025-06-28#bankpacific_transactions_2025-06-28.csv",
  "fileId": "FILE#bankpacific#bankpacific_transactions_2025-06-28.csv",
  "fileName": "bankpacific_transactions_2025-06-28.csv",
  "customerId": "bankpacific",
  "status": "SUCCESS",
  "workflowId": "copy-sftp-to-s3-and-sftp",
  "targetSummary": {
    "s3": "s3://archive-bucket-secure/bankpacific/2025-06/",
    "sftp": "sftp://aws-transfer/bankpacific/partner-dropzone/"
  },
  "retryCount": 1,
  "timestamp": "2025-06-28T22:01:34Z",
  "errorMessage": null
}
```

---

## 🔍 **Common Access Patterns Enabled**

| Query Scenario                                    | Example                                                          |
| ------------------------------------------------- | ---------------------------------------------------------------- |
| Get all files for a customer on a date            | `PK = CUSTOMER#bankpacific` and `SK begins_with DATE#2025-06-28` |
| List all files processed by a customer this month | Filter by `SK starts_with DATE#2025-06`                          |
| Show all failed files for a customer              | Query + filter by `status = FAILED`                              |
| Link to full transfer history                     | Use `fileId` to fetch from `FileTransferStatus` table            |

---

## 🧠 Design Notes

* This table acts like a **secondary index view**, purpose-built for **lookup & display**.
* Denormalized intentionally to **avoid expensive joins** in DynamoDB.
* Can be exported to S3 for reporting or analytics in Athena / QuickSight.

---

## 🔄 When is the item inserted?

You should write to this table **at the end of your Step Function**, when the file transfer is:

* Marked **SUCCESS**
* Or marked **FAILED after max retries**

You can also **upsert** it each time a retry happens, if you want real-time display of retry attempts.

---

## 🛠️ Python (Boto3) Upsert Example

```python
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CustomerFileIndex')

def write_customer_file_index(event):
    customer = event['customerId']
    file = event['fileName']
    date_part = event['timestamp'].split('T')[0]

    table.put_item(
        Item={
            'PK': f'CUSTOMER#{customer}',
            'SK': f'DATE#{date_part}#{file}',
            'fileId': event['fileId'],
            'fileName': file,
            'customerId': customer,
            'status': event['status'],
            'workflowId': event['workflowId'],
            'targetSummary': event['target'],
            'retryCount': event['retryCount'],
            'timestamp': event['timestamp'],
            'errorMessage': event.get('errorMessage', None)
        }
    )
```

---

## 🧭 Summary

| Feature                         | Purpose                                              |
| ------------------------------- | ---------------------------------------------------- |
| `PK = CUSTOMER#<client>`        | Groups all files per customer                        |
| `SK = DATE#<yyyy-mm-dd>#<file>` | Enables sort/filter by date and file                 |
| Denormalized summary            | Supports fast rendering of status in UI              |
| `fileId` back reference         | Enables join to full history in `FileTransferStatus` |



+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Let’s now explore the **`WorkflowDefinition`** DynamoDB table in detail — this is key for enabling a **self-serve, dynamic, and extensible file transfer system**.

---

## ✅ **Table: `WorkflowDefinition`**

### 📌 **Purpose**

Store **declarative definitions** of all file transfer workflows, so Step Functions and Lambda functions can dynamically read configurations without hardcoding logic.

This allows:

* Self-service onboarding of new clients
* Dynamic routing logic
* Support for multiple file transfer patterns (SFTP → S3, S3 → SFTP, etc.)
* Easy updates to file validation, retries, and target destinations

---

## 🧩 **Key Schema**

| Key Type      | Key Name | Example Value              |
| ------------- | -------- | -------------------------- |
| Partition Key | `PK`     | `WORKFLOW#copy-sftp-to-s3` |

This design uniquely identifies each workflow by `workflowId`.

---

## 📋 **Attributes**

| Attribute         | Type    | Description                                                               |
| ----------------- | ------- | ------------------------------------------------------------------------- |
| `PK`              | String  | Primary key: `WORKFLOW#<workflowId>`                                      |
| `workflowId`      | String  | ID of the workflow (e.g., `copy-sftp-to-s3`)                              |
| `sourceType`      | String  | Type of source: `SFTP`, `S3`                                              |
| `targetType`      | String  | Type of target: `S3`, `SFTP`, `S3_SFTP`, etc.                             |
| `sourcePrefix`    | String  | Optional S3 or path prefix to validate source files                       |
| `target`          | Map     | Default target config (S3 bucket path, SFTP backend folder)               |
| `validationRegex` | String  | Regex to validate file naming convention (e.g., `.csv$`)                  |
| `maxRetries`      | Number  | Default max retry count for file transfer                                 |
| `stepFunctionArn` | String  | ARN of the associated Step Function                                       |
| `enabled`         | Boolean | If `false`, this workflow is disabled for execution                       |
| `tags`            | Map     | Custom tags or labels (e.g., `{"business": "finance", "region": "west"}`) |
| `createdAt`       | String  | ISO timestamp when the workflow was created                               |
| `updatedAt`       | String  | ISO timestamp when the workflow was last updated                          |

---

## 🧾 **Sample Item: SFTP → S3 Workflow**

```json
{
  "PK": "WORKFLOW#copy-sftp-to-s3",
  "workflowId": "copy-sftp-to-s3",
  "sourceType": "SFTP",
  "targetType": "S3",
  "sourcePrefix": "from-sftp/",
  "target": {
    "bucket": "s3://archive-bucket/",
    "pathPattern": "customerId/YYYY/MM/"
  },
  "validationRegex": "^client[a-zA-Z]+_transactions_\\d{4}-\\d{2}-\\d{2}\\.csv$",
  "maxRetries": 3,
  "stepFunctionArn": "arn:aws:states:us-west-2:123456789012:stateMachine:copy-sftp-to-s3-sm",
  "enabled": true,
  "tags": {
    "business": "finance",
    "region": "west"
  },
  "createdAt": "2025-06-01T10:00:00Z",
  "updatedAt": "2025-06-28T10:00:00Z"
}
```

---

## 🔍 **Use Cases Enabled**

| Use Case                                       | How `WorkflowDefinition` Helps                             |
| ---------------------------------------------- | ---------------------------------------------------------- |
| Add a new customer onboarding pattern          | Insert new item with `workflowId` and routing logic        |
| Support multiple source-target types           | Define combinations like S3 → SFTP, SFTP → SFTP, etc.      |
| Step Function or Lambda decides routing        | Dynamically loads target from table, no code change needed |
| Validate filenames                             | Reads `validationRegex` and checks in Lambda               |
| Route to different targets by file type/client | Use `pathPattern` or tag rules in the record               |

---

## 🧠 Best Practices

* Keep **one record per `workflowId`**
* Use **Lambda cache** to avoid re-fetching unchanged workflows
* Use **CloudWatch Metrics** to track which workflows are active or failing
* Optionally **encrypt** sensitive fields using AWS KMS

---

## 🔄 Example Workflow Routing Flow

```text
EventBridge → SQS → Step Function
            |
            ▼
   Read `workflowId` from SQS Message
            |
            ▼
   Fetch `WorkflowDefinition` from DynamoDB
            |
            ▼
   Use validationRegex, maxRetries, and target in transfer logic
```

---

## 🔐 IAM Policy to Read from Table

```json
{
  "Effect": "Allow",
  "Action": ["dynamodb:GetItem"],
  "Resource": "arn:aws:dynamodb:<region>:<account-id>:table/WorkflowDefinition"
}
```

---

## ✅ Summary

| Feature                         | Benefit                                                          |
| ------------------------------- | ---------------------------------------------------------------- |
| Dynamic Routing                 | No hardcoding of logic in Lambda or Step Function                |
| Supports Multi-Client Workflows | Easy to onboard new customers and transfer logic                 |
| Validation-Driven               | Prevents bad files or wrong patterns from entering pipeline      |
| Extensible                      | Add new targets, retry policies, or workflow states with no code |

---

![image](https://github.com/user-attachments/assets/8dddf66a-4b67-4056-96fb-0638ce963124)



Let’s now walk through the **`FileTransferAuditLog`** table — an optional but highly valuable DynamoDB table in your architecture used to maintain **append-only historical logs** of all file transfer activities.

---

## ✅ **Table: `FileTransferAuditLog`**

### 📌 Purpose:

Store **every event or state change** in a file’s lifecycle — from upload, validation, routing, retries, to final success/failure.

It is:

* **Append-only** (write-only, never update)
* Ideal for **audit trails**, **compliance**, **analytics**, and **debugging**
* Linked to the `FileTransferStatus` table (but captures *all steps*, not just latest)

---

## 🧩 Key Schema

| Key Type      | Key Name | Example Value                                  |
| ------------- | -------- | ---------------------------------------------- |
| Partition Key | `PK`     | `FILE#bankpacific_transactions_2025-06-28.csv` |
| Sort Key      | `SK`     | `TS#2025-06-28T21:02:55Z`                      |

This schema allows **time-ordered logs per file**.

---

## 📋 Attributes

| Attribute        | Type   | Description                                                                                               |
| ---------------- | ------ | --------------------------------------------------------------------------------------------------------- |
| `PK`             | String | Partition key: always in format `FILE#<fileName>`                                                         |
| `SK`             | String | Sort key: timestamp prefixed with `TS#`                                                                   |
| `eventType`      | String | The stage or operation (e.g., `UPLOAD_RECEIVED`, `VALIDATED`, `COPY_TO_S3`, `RETRY`, `SUCCESS`, `FAILED`) |
| `status`         | String | Status after this event (e.g., `IN_PROGRESS`, `FAILED`)                                                   |
| `retryCount`     | Number | Retry count at that point in time                                                                         |
| `workflowId`     | String | ID of the workflow that was active during this event                                                      |
| `stepFunctionId` | String | Execution ID of the Step Function                                                                         |
| `customerId`     | String | Name or ID of the customer                                                                                |
| `message`        | String | Log message or error description                                                                          |
| `metadata`       | Map    | Optional additional metadata (file size, region, actor, etc.)                                             |

---

## 🧾 Example AuditLog Record

```json
{
  "PK": "FILE#bankpacific_transactions_2025-06-28.csv",
  "SK": "TS#2025-06-28T21:02:55Z",
  "eventType": "RETRY",
  "status": "IN_PROGRESS",
  "retryCount": 2,
  "workflowId": "copy-sftp-to-s3-and-sftp",
  "stepFunctionId": "execution-abc-123",
  "customerId": "bankpacific",
  "message": "Retrying file transfer to S3. Previous attempt failed due to timeout.",
  "metadata": {
    "region": "us-west-2",
    "handler": "lambda_sftp_to_s3",
    "durationMs": 1173
  }
}
```

---

## 🔍 Use Cases & Access Patterns

| Use Case                                         | How it works                                            |
| ------------------------------------------------ | ------------------------------------------------------- |
| View full lifecycle of a file                    | Query by `PK = FILE#<fileName>`, sort by `SK` ascending |
| Filter only failed events for a file             | Query by PK, filter by `status = FAILED`                |
| Compliance/audit reporting                       | Export logs to S3 and run Athena or QuickSight on them  |
| Group by `eventType`, `customerId` for reporting | Use DDB → Firehose → S3 export → Athena for queries     |

---

## 💡 Example Audit Log Timeline for a File

| Timestamp            | Event Type        | Status        | Retry Count | Message                                      |
| -------------------- | ----------------- | ------------- | ----------- | -------------------------------------------- |
| 2025-06-28T21:01:00Z | `UPLOAD_RECEIVED` | `PENDING`     | 0           | File landed in S3 via AWS Transfer Family    |
| 2025-06-28T21:01:10Z | `VALIDATED`       | `IN_PROGRESS` | 0           | Filename format passed                       |
| 2025-06-28T21:01:30Z | `COPY_TO_S3`      | `FAILED`      | 0           | S3 Access Denied                             |
| 2025-06-28T21:02:55Z | `RETRY`           | `IN_PROGRESS` | 2           | Retrying file transfer to S3                 |
| 2025-06-28T21:03:50Z | `SUCCESS`         | `SUCCESS`     | 2           | File successfully transferred to all targets |

---

## 🔐 IAM Policy (to Write to Audit Table)

```json
{
  "Effect": "Allow",
  "Action": ["dynamodb:PutItem"],
  "Resource": "arn:aws:dynamodb:<region>:<account>:table/FileTransferAuditLog"
}
```

---

## 🧠 Best Practices

* Make this table **append-only** (no overwrites)
* Use **Time-to-Live (TTL)** if you want to auto-delete old logs (e.g., after 1 year)
* Use **DynamoDB Streams → Firehose → S3** to export for audit/BI
* Consider writing to **CloudWatch Logs** and `FileTransferAuditLog` in parallel (for real-time and historical logging)

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


Let’s now deep-dive into the **`TransferFailureQueue`** DynamoDB table — an important component in your file transfer architecture used to **persistently track files that failed** even after all retry attempts.

---

## ✅ **Table: `TransferFailureQueue`**

### 📌 Purpose:

Capture **permanently failed** file transfers that:

* Exceeded their maximum retry limit in Step Functions
* Require **manual intervention** or re-processing later
* Should be reviewed by operations/support teams

---

## 🧩 Key Schema

| Key Type      | Key Name | Example Value                                     |
| ------------- | -------- | ------------------------------------------------- |
| Partition Key | `PK`     | `FAILURE#bankpacific_transactions_2025-06-28.csv` |

This ensures one record per failed file (latest failure).

---

## 📋 Attributes

| Attribute        | Type   | Description                                                                |
| ---------------- | ------ | -------------------------------------------------------------------------- |
| `PK`             | String | Primary key in format: `FAILURE#<fileName>`                                |
| `fileName`       | String | Name of the file that failed                                               |
| `customerId`     | String | Client who submitted the file                                              |
| `status`         | String | Always `FAILED`                                                            |
| `workflowId`     | String | The workflow that failed (e.g., `copy-sftp-to-s3`)                         |
| `retryCount`     | Number | Number of attempts made before giving up                                   |
| `errorMessage`   | String | Last error message returned by the Lambda or Step Function                 |
| `failureReason`  | String | Optional: custom mapped reason code (e.g., `PERMISSION_DENIED`, `TIMEOUT`) |
| `stepFunctionId` | String | Execution ID for debugging                                                 |
| `timestamp`      | String | When the failure was recorded (ISO 8601)                                   |
| `metadata`       | Map    | Optional map: region, lambda function, retry history, etc.                 |

---

## 🧾 Sample Record

```json
{
  "PK": "FAILURE#bankpacific_transactions_2025-06-28.csv",
  "fileName": "bankpacific_transactions_2025-06-28.csv",
  "customerId": "bankpacific",
  "status": "FAILED",
  "workflowId": "copy-sftp-to-s3-and-sftp",
  "retryCount": 3,
  "errorMessage": "AccessDenied: S3 bucket not found or IAM role misconfigured.",
  "failureReason": "PERMISSION_DENIED",
  "stepFunctionId": "exec-1234-abc",
  "timestamp": "2025-06-28T22:15:03Z",
  "metadata": {
    "region": "us-west-2",
    "lambda": "lambda_sftp_to_s3",
    "fileSizeBytes": 4293123
  }
}
```

---

## 🔍 Use Cases & Benefits

| Use Case                                     | Description                                                           |
| -------------------------------------------- | --------------------------------------------------------------------- |
| Post-mortem investigation                    | Engineers or support can review `errorMessage` and `stepFunctionId`   |
| Manual re-processing                         | Admins can re-submit failed files via UI/API                          |
| Customer communication                       | Helpdesk teams can notify clients of the failure with clear messages  |
| Metrics dashboard                            | Count of failed files per client, per workflow, per reason            |
| Clean separation of **active** vs **failed** | Keeps `FileTransferStatus` lightweight for recent success/in-progress |

---

## 🔁 When to Write

You write to this table **after all retries have failed** in your Step Function — typically from a `Log Failure` Lambda state.

---

## 🛠️ Lambda: Sample Write to `TransferFailureQueue`

```python
import boto3
import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TransferFailureQueue')

def write_failure_record(file_name, customer_id, workflow_id, retry_count, error_msg, step_fn_id, failure_reason, metadata):
    timestamp = datetime.datetime.utcnow().isoformat()

    item = {
        'PK': f'FAILURE#{file_name}',
        'fileName': file_name,
        'customerId': customer_id,
        'status': 'FAILED',
        'workflowId': workflow_id,
        'retryCount': retry_count,
        'errorMessage': error_msg,
        'failureReason': failure_reason,
        'stepFunctionId': step_fn_id,
        'timestamp': timestamp,
        'metadata': metadata or {}
    }

    table.put_item(Item=item)
```

---

## 🔐 IAM Policy

```json
{
  "Effect": "Allow",
  "Action": ["dynamodb:PutItem"],
  "Resource": "arn:aws:dynamodb:<region>:<account>:table/TransferFailureQueue"
}
```

---

## 📈 Optional Enhancements

| Feature                   | Value                                                 |
| ------------------------- | ----------------------------------------------------- |
| TTL enabled               | Auto-expire records older than 30 days if reprocessed |
| GSI on `customerId`       | To list all failures per customer (dashboard or API)  |
| Filter by `failureReason` | For trending root causes and mitigation tracking      |
| SNS alert integration     | Trigger alerts when a new failure is logged           |

![image](https://github.com/user-attachments/assets/84aea64c-8cc8-4a3d-abc9-58a8f6fbcc3b)



Let’s now walk through the **`TransferNotificationLog`** DynamoDB table — designed to track all notifications triggered by your file transfer workflow, such as **email alerts**, **SNS messages**, or **webhooks**.

---

## ✅ **Table: `TransferNotificationLog`**

### 📌 **Purpose**

Keep a log of **when, how, and to whom** a notification was sent, for auditing, support, and traceability.

It helps:

* Prove notification delivery (for compliance)
* Avoid duplicate alerts
* Debug missing notifications
* Track webhook performance or failure

---

## 🧩 **Key Schema**

| Key Type      | Key Name | Example Value                                    |
| ------------- | -------- | ------------------------------------------------ |
| Partition Key | `PK`     | `NOTIFY#bankpacific_transactions_2025-06-28.csv` |
| Sort Key      | `SK`     | `TS#2025-06-28T22:01:35Z`                        |

---

## 📋 **Attributes**

| Attribute    | Type   | Description                                                          |
| ------------ | ------ | -------------------------------------------------------------------- |
| `PK`         | String | Notification log per file (`NOTIFY#<fileName>`)                      |
| `SK`         | String | Timestamp of the notification (`TS#<ISO timestamp>`)                 |
| `fileName`   | String | The name of the file associated with this notification               |
| `customerId` | String | The client ID                                                        |
| `status`     | String | `SENT`, `FAILED`, `RETRYING`                                         |
| `type`       | String | `SNS`, `EMAIL`, `WEBHOOK`, `TEAMS`, etc.                             |
| `target`     | String | Destination endpoint (email address, webhook URL, SNS topic ARN)     |
| `messageId`  | String | ID returned by service (e.g., SNS message ID or HTTP response ID)    |
| `response`   | String | Status message from provider (e.g., HTTP 200, SNS message delivered) |
| `retryCount` | Number | Retry attempts made                                                  |
| `workflowId` | String | Workflow associated with this file transfer                          |
| `timestamp`  | String | ISO timestamp (redundant with SK for queries)                        |
| `metadata`   | Map    | Optional: region, source Lambda, error trace, etc.                   |

---

## 🧾 **Sample Record**

```json
{
  "PK": "NOTIFY#bankpacific_transactions_2025-06-28.csv",
  "SK": "TS#2025-06-28T22:01:35Z",
  "fileName": "bankpacific_transactions_2025-06-28.csv",
  "customerId": "bankpacific",
  "status": "SENT",
  "type": "SNS",
  "target": "arn:aws:sns:us-west-2:123456789012:file-transfer-notify",
  "messageId": "b7f57d33-4fbf-490c-832c-52d157b92c31",
  "response": "Message published to SNS",
  "retryCount": 0,
  "workflowId": "copy-sftp-to-s3-and-sftp",
  "timestamp": "2025-06-28T22:01:35Z",
  "metadata": {
    "region": "us-west-2",
    "lambda": "lambda_send_notification"
  }
}
```

---

## 🔍 **Use Cases**

| Use Case                          | Query Example                                                    |
| --------------------------------- | ---------------------------------------------------------------- |
| View all notifications for a file | Query by `PK = NOTIFY#<fileName>`                                |
| Audit all alerts sent to client   | Filter by `customerId` and `type`                                |
| Analyze failures for retry        | Query by `status = FAILED`                                       |
| Re-publish failed messages        | Fetch `target`, `messageId`, and `message body` for reprocessing |
| Daily notification metrics        | Count by `workflowId`, `type`, or `status`                       |

---

## 🧠 Best Practices

* Write a log **after** SNS publish, webhook POST, or email send.
* On `FAILED` or `RETRYING`, include failure reason in `response`.
* Enable **TTL** to purge logs older than X days if logs are exported to S3.

---

## 🛠️ Lambda Snippet: Write Notification Log

```python
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TransferNotificationLog')

def log_notification(file_name, customer_id, status, notif_type, target, msg_id, response_msg, retry_count, workflow_id, metadata=None):
    timestamp = datetime.utcnow().isoformat()
    pk = f"NOTIFY#{file_name}"
    sk = f"TS#{timestamp}"
    
    item = {
        "PK": pk,
        "SK": sk,
        "fileName": file_name,
        "customerId": customer_id,
        "status": status,
        "type": notif_type,
        "target": target,
        "messageId": msg_id,
        "response": response_msg,
        "retryCount": retry_count,
        "workflowId": workflow_id,
        "timestamp": timestamp,
        "metadata": metadata or {}
    }
    
    table.put_item(Item=item)
```

---

## 🧪 Example Athena Query (If Logs Exported to S3)

```sql
SELECT customerId, COUNT(*) as notifications, status
FROM transfer_notification_log
WHERE timestamp > current_date - interval '7' day
GROUP BY customerId, status
ORDER BY notifications DESC;
```

---

Here’s a detailed concept for both a **Slack/Teams bot** and a **dashboard** to monitor `TransferNotificationLog` data in real-time and improve observability for your file transfer pipeline.

---

## 🤖 Slack or Microsoft Teams Bot Concept

### ✅ Bot Name: `TransferAlertBot`

---

### 🔧 **Bot Capabilities**

| Command                              | Description                                                     |
| ------------------------------------ | --------------------------------------------------------------- |
| `/transfer-status <fileName>`        | Fetches latest notification status for a file                   |
| `/transfer-notifications <customer>` | Lists recent notifications for a customer                       |
| `/transfer-failed-notifications`     | Lists last 5 failed notifications across the system             |
| `/transfer-retry <fileName>`         | Triggers re-send logic (calls Lambda or Step Function to retry) |
| `/transfer-alert-summary`            | Summary of notifications by status (past 24h or 7d)             |

---

### 📥 Sample Bot Interaction (Slack)

```
👤 User:
/transfer-status bankpacific_transactions_2025-06-28.csv

🤖 TransferAlertBot:
📄 *File:* `bankpacific_transactions_2025-06-28.csv`
👤 *Customer:* `bankpacific`
🛠 *Workflow:* `copy-sftp-to-s3-and-sftp`
📣 *Notification Type:* SNS  
✅ *Status:* SENT  
📬 *Sent To:* arn:aws:sns:us-west-2:123:file-transfer-notify  
🕒 *Time:* 2025-06-28T22:01:35Z
📎 *Message ID:* b7f57d33-4fbf-490c-832c-52d157b92c31
```

---

### ⚙️ Tech Stack

| Component       | Description                                      |
| --------------- | ------------------------------------------------ |
| Slack/Teams App | Built with Bolt (Slack) or Bot Framework (Teams) |
| AWS Lambda      | Backend for each bot command (Python)            |
| DynamoDB        | Reads from `TransferNotificationLog`             |
| API Gateway     | Optional for webhook endpoints                   |
| IAM Role        | Read-only access to DynamoDB                     |

---

### 🔐 IAM Permissions

```json
{
  "Effect": "Allow",
  "Action": ["dynamodb:Query", "dynamodb:GetItem"],
  "Resource": "arn:aws:dynamodb:<region>:<account>:table/TransferNotificationLog"
}
```

---

## 📊 Notification Health Dashboard

### 🖥️ Platform Options

* **Amazon QuickSight** (built on S3 export + Athena)
* **Grafana** (using CloudWatch + Lambda metrics)
* **Tableau or Power BI** (if exported to Redshift or S3)

---

### 📈 Key Metrics to Visualize

| Metric                                 | Chart Type           |
| -------------------------------------- | -------------------- |
| Notifications sent per customer        | Bar or Pie Chart     |
| Failed notifications (7-day trend)     | Line or Area Chart   |
| Delivery time latency per notification | Box or Histogram     |
| SNS/Webhook response errors            | Table + Bar          |
| Retry attempts distribution            | Line or Scatter Plot |
| Notification type usage (SNS, Email…)  | Donut Chart          |

---

### 📊 Example Dashboard Cards

1. ✅ **Success vs Failed Notification Ratio**
2. 📉 **Top 5 Customers with Most Notification Failures**
3. 🧭 **Average Notification Latency per Workflow**
4. 🛠️ **Real-Time Table of Recent Failed Notifications**
5. 📬 **Last 10 Notification Messages Sent**

---

### 🔁 Data Source Options

* Use **DynamoDB Streams → Kinesis Firehose → S3**
* Or schedule a Lambda to export logs to **S3 as JSON**
* Use AWS Glue Crawler → Athena → QuickSight

---

✅ All three deliverables are now available:

### 1. **Terraform Slack Bot Module**

* Deploys a Lambda-powered Slack bot behind an API Gateway.
* Located in: `Terraform Slack Bot Module`

### 2. **Athena + Glue Export Setup**

* Exports `TransferNotificationLog` from DynamoDB to S3 using Glue.
* Located in: `Athena Glue Export Setup`

### 3. **Grafana Notification Dashboard**

* Visualizes CloudWatch metrics: sent/failure trends, error tables, and volume by customer.
* Located in: `Grafana Notification Dashboard`

Would you like:

* A combined deployment guide for all three components?
* Or integration instructions to wire all of these together in one CI/CD flow?




Absolutely! Let’s explain in detail the use of **Global Secondary Indexes (GSI)** in the context of your DynamoDB-based file transfer architecture, specifically for tables like:

* `FileTransferStatus`
* `TransferNotificationLog`
* `TransferFailureQueue`

---

## 🧠 What is a GSI (Global Secondary Index)?

A **Global Secondary Index** allows you to query your DynamoDB table **on attributes other than the primary key** (i.e., PK/SK).

* You define a **GSI partition key** and an optional **sort key**.
* You can project additional attributes to the GSI for efficient querying.
* Unlike the base table’s key schema, **GSI queries are flexible** and support **filtering, sorting, and alternate access patterns**.

---

## 🔍 Why Use GSIs in File Transfer Architecture?

DynamoDB tables like `FileTransferStatus` are designed for **file-specific tracking** using `PK = FILE#<customerId>#<fileName>`. But if you want to:

* List all transfers by a **customer ID**
* Get all **FAILED** transfers by a **workflow**
* View all files transferred on a **given day**

—you **need GSIs**, because those fields are not part of the base key.

---

## ✅ Recommended Global Secondary Indexes (GSIs)

### ✅ GSI #1: `CustomerIndex`

| Field                  | Purpose                 |
| ---------------------- | ----------------------- |
| Partition Key (GSI1PK) | `customerId`            |
| Sort Key (GSI1SK)      | `timestamp` or `status` |

#### 🔹 Use Case:

* Show all files processed by a specific customer
* Filter by date or status (success/failure)

---

### ✅ GSI #2: `WorkflowStatusIndex`

| Field                  | Purpose      |
| ---------------------- | ------------ |
| Partition Key (GSI2PK) | `workflowId` |
| Sort Key (GSI2SK)      | `status`     |

#### 🔹 Use Case:

* Count how many files **failed** under a specific workflow
* Monitor health of each routing path

---

### ✅ GSI #3: `DateStatusIndex` (Optional for BI use)

| Field                  | Purpose                 |
| ---------------------- | ----------------------- |
| Partition Key (GSI3PK) | `date` (from timestamp) |
| Sort Key (GSI3SK)      | `status`                |

#### 🔹 Use Case:

* Daily transfer success/failure rates
* Aggregate by status over time

---

## 🧩 Example for `FileTransferStatus` Table

### Base Table Key Schema:

| PK                                         | SK                        |
| ------------------------------------------ | ------------------------- |
| `FILE#bankpacific#transactions_2025-06-28` | `TS#2025-06-28T21:01:00Z` |

### GSI: `CustomerIndex`

| GSI1PK        | GSI1SK       | status  | fileName         | timestamp           |
| ------------- | ------------ | ------- | ---------------- | ------------------- |
| `bankpacific` | `2025-06-28` | SUCCESS | transactions.csv | `2025-06-28T21:01Z` |

You can now run queries like:

```sql
GSI1PK = 'bankpacific'
AND GSI1SK BETWEEN '2025-06-27' AND '2025-06-29'
```

---

## 🛠️ Terraform GSI Example for FileTransferStatus

```hcl
global_secondary_index {
  name            = "CustomerIndex"
  hash_key        = "customerId"
  range_key       = "timestamp"
  projection_type = "ALL"
  read_capacity   = 5
  write_capacity  = 5
}
```

---

## 🔄 Projected Attributes

When you define a GSI, you can specify:

* `KEYS_ONLY`: Just PK and SK
* `INCLUDE`: Specific attributes (e.g., `status`, `workflowId`)
* `ALL`: Full item copy (easiest for reporting, higher cost)

---

## 📈 Best Practices

| Tip                                                  | Why it Helps                                               |
| ---------------------------------------------------- | ---------------------------------------------------------- |
| Use ISO date parts in sort keys                      | Enables range queries (e.g., `2025-06-01` to `2025-06-30`) |
| Keep indexes sparse                                  | Avoid indexing attributes not used in filtering            |
| Consider write cost implications                     | Each write incurs cost for every GSI it updates            |
| Use **GSI for dashboard data**, not detailed history | Keep main table for workflow logic; GSI for analytics      |

---

## ✅ Summary Table of Suggested GSIs

| Table Name                | GSI Name                    | PK Field     | SK Field    | Use Case                             |
| ------------------------- | --------------------------- | ------------ | ----------- | ------------------------------------ |
| `FileTransferStatus`      | `CustomerIndex`             | `customerId` | `timestamp` | Show all files for a customer        |
| `FileTransferStatus`      | `WorkflowStatusIndex`       | `workflowId` | `status`    | Track workflow health                |
| `TransferNotificationLog` | `NotificationCustomerIndex` | `customerId` | `status`    | Failed alerts per customer           |
| `TransferFailureQueue`    | `FailureByCustomer`         | `customerId` | `timestamp` | Reprocess all failed files by client |

---

Here is the updated **Entity-Relationship Diagram (ERD)** that includes all your DynamoDB Global Secondary Indexes (GSIs) for the file transfer pipeline:

📌 **[Click to view or download the ERD with GSIs »](sandbox:/mnt/data/updated_dynamodb_erd_with_gsi.png)**

---

Next, here are a few Athena query examples assuming your DynamoDB tables are exported to S3:

---

### 📊 **Athena Query: List Failed Files by Workflow**

```sql
SELECT fileName, customerId, status, timestamp
FROM file_transfer_status
WHERE workflowId = 'copy-sftp-to-s3'
  AND status = 'FAILED'
ORDER BY timestamp DESC;
```

---

### 📊 **Athena Query: Get All File Status for a Customer in Last 7 Days**

```sql
SELECT fileName, status, timestamp
FROM file_transfer_status
WHERE customerId = 'bankpacific'
  AND timestamp > date_format(current_timestamp - interval '7' day, '%Y-%m-%d')
ORDER BY timestamp DESC;
```

---

### 📊 **Athena Query: Summary by Status**

```sql
SELECT status, COUNT(*) AS total_files
FROM file_transfer_status
GROUP BY status;
```


















