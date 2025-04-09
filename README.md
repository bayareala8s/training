Firehose delivers syslog data from Amazon Kinesis Data Streams into an S3 staging bucket for storage, processing, or further analytics.

Kinesis Data Firehose acts as a delivery pipeline between Kinesis Data Streams and Amazon S3.

Firehose is Configured with a Kinesis Source
The Firehose delivery stream is linked to your existing Kinesis Data Stream (e.g., AppianLogsStream).

It polls Kinesis for new records using an IAM role.

Buffering and Batching
Firehose buffers incoming data using two parameters:

Buffer size (e.g., 5 MB)

Buffer interval (e.g., 300 seconds)

It writes to S3 when either condition is met, whichever happens first.

Example: If 5 MB of logs arrive in 60 seconds, the batch is flushed immediately.

Writes to Amazon S3
The data is stored in compressed or raw format (depending on config).

Files are organized by date:

bash
Copy
Edit
s3://appian-log-staging-bucket/YYYY/MM/DD/HH/appian-logs.gz
