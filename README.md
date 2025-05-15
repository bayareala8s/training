Step 4: Define Required Slots (Fields)
Add the following slots to the intent with appropriate prompts:

Slot Name	Type	Prompt
customerId	Amazon.AlphaNumeric	What is the customer ID?
environment	Custom (dev/test/prod)	What environment is this for?
workflowId	Custom (sftp-to-s3, s3-to-sftp)	What is the workflow type?
sourceType	Literal (SFTP)	What is the source type?
sourceHost	Amazon.AlphaNumeric	Enter the source SFTP hostname
sourcePort	Amazon.Number	What is the SFTP port?
sourceUsername	Amazon.AlphaNumeric	What is the SFTP username?
authMethod	Custom (ssh_key, password)	What is the authentication method?
authKey	Amazon.AlphaNumeric	Provide SSH key name or password
sourcePath	Amazon.AlphaNumeric	What is the file path on the SFTP server?
destBucket	Amazon.AlphaNumeric	What is the S3 bucket name?
destPrefix	Amazon.AlphaNumeric	What is the folder/prefix in the S3 bucket?
cronSchedule	Amazon.AlphaNumeric	What is the cron expression for scheduling?
