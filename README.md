Component	Subnet	Reason / Role
ECS Fargate Tasks (Syslog Receiver)	Private Subnet	Secured; not exposed directly to the internet. Receives traffic from NLB only.
Kinesis Data Streams	AWS Managed	Not in your VPC. Accessed via public endpoints or VPC Interface Endpoints.
Kinesis Firehose	AWS Managed	Fully managed by AWS. Firehose pulls data from Streams and writes to S3.
Amazon S3 (Staging Bucket)	AWS Managed	Not in your VPC. Access via S3 Gateway or Interface Endpoint recommended.
CloudWatch Logs	AWS Managed	ECS task logs go here. Accessible via Interface VPC Endpoint if private.
VPC Interface Endpoints (PrivateLink)	Private Subnet	Enables secure, private access to Kinesis, S3, CloudWatch, etc., from ECS.
