## **Summary of the Self-Serve JSON-Based AWS File Transfer Automation Workflow**

### **Objective**
The workflow enables customers to define their file transfer configuration in a JSON file, and Terraform dynamically provisions the required AWS resources — including a Python Lambda function — to automatically copy files from a **source S3 bucket** to a **target S3 bucket** upon file upload.

---

## **Workflow Overview**
The process is structured into five key stages:

---

### **Step 1: JSON Configuration**
- The customer defines their desired setup in a JSON file (`config.json`).  
- This JSON file specifies:
  - **Source Bucket**
  - **Target Bucket**
  - **Lambda Configuration** (runtime, timeout, memory)
  - **CloudWatch Logs Configuration** (log group name and retention period)  

✅ This ensures each customer’s setup is flexible and requires no manual intervention.

---

### **Step 2: Terraform Automation**
- Terraform reads the JSON configuration and:
  - Creates the **Source** and **Target** S3 buckets.
  - Deploys the **Python Lambda function** for file transfer.
  - Assigns **IAM roles and policies** to grant the Lambda function access to the S3 buckets.
  - Configures **CloudWatch Logs** for monitoring.
  - Sets up **S3 Event Notifications** to automatically trigger the Lambda function when a file is uploaded to the **Source bucket**.

✅ This fully automated setup ensures all required AWS resources are dynamically provisioned.

---

### **Step 3: Lambda Function Execution**
- When a new file is uploaded to the **Source Bucket**, the following steps occur:
  1. **S3 Event Notification** triggers the Lambda function.
  2. The Lambda function reads the environment variable containing the JSON configuration.
  3. The Lambda function identifies the newly uploaded file and copies it to the **Target Bucket**.
  4. The Lambda function logs the success/failure of the operation in **CloudWatch Logs**.

✅ This automated copying process requires no manual intervention.

---

### **Step 4: Monitoring and Logging**
- The Lambda function writes detailed logs for:
  - **Successful file transfers**
  - **Errors or permission issues**
  - **General execution metrics**
- Customers can monitor these logs using CloudWatch for improved visibility and troubleshooting.

✅ This ensures easy debugging and tracking of file transfers.

---

### **Step 5: Testing and Validation**
- The solution can be tested by:
  1. Uploading a sample file to the **Source Bucket**.
  2. Verifying the file appears in the **Target Bucket**.
  3. Checking **CloudWatch Logs** for Lambda execution details.

✅ This ensures that all components are working as expected.

---

## **End-to-End Workflow Diagram**
```
+-------------------+        +------------------+
|   JSON Config       |        |  Terraform Deploy |
|  (config.json)      |        |  AWS Resources    |
+-------------------+        +------------------+
           |                          |
           v                          v
+-------------------+        +------------------+
|    AWS S3 Bucket    |        |     AWS Lambda    |
|    (Source Bucket)   |        | (Python Function) |
+-------------------+        +------------------+
           |                          |
           |       S3 Event Trigger    |
           +------------------------->|
                                        |
                                        v
                               +------------------+
                               |  AWS S3 Bucket    |
                               |  (Target Bucket)   |
                               +------------------+
                                        |
                                        v
                               +------------------+
                               |  CloudWatch Logs   |
                               |  (Success/Failure)  |
                               +------------------+
```

---

## **Key Benefits**
✅ **Flexible Configuration** – Customers define settings in JSON for easy customization.  
✅ **Automation** – Terraform handles resource creation and Lambda deployment.  
✅ **Scalability** – Automatically scales as new files arrive.  
✅ **Enhanced Monitoring** – CloudWatch tracks file movement, errors, and success.  
✅ **Cost-Efficiency** – Fully serverless architecture with pay-per-use pricing.

---

Would you like guidance on additional features like retries, error handling, or email notifications for failures? 🚀
