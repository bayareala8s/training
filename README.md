AWS Fargate is used to run the containerized Syslog Receiver that accepts logs from Appian Cloud and forwards them to Amazon Kinesis Data Streams.

Workflow: How Fargate Receives and Forwards Logs
1. Appian Cloud sends UDP logs to Fargate task
UDP traffic is allowed via security group inbound rule on port 514

Task is assigned a public IP in a public subnet

2. Fargate runs a container with rsyslog
The Docker container listens on UDP port 514 using rsyslog

Incoming logs are piped to a Python script

3. Python script forwards logs to Kinesis
Using AWS SDK (boto3), the container sends logs to Amazon Kinesis Data Streams
