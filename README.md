Kinesis Data Streams serves as the real-time transport layer, moving log events from the Syslog receiver (Fargate container) to Amazon S3 via Firehose — without loss, delay, or manual scaling.

he Fargate-based syslog receiver uses the AWS SDK (boto3) to call:

python
Copy
Edit
put_record(StreamName="AppianLogsStream", Data=log_json, PartitionKey="syslog")

KDS splits incoming data across “shards.”

Each shard can handle:

1 MB/sec ingress

2 MB/sec egress

1000 records/sec

Delivery via Firehose
You create a Kinesis Firehose that:

Sources data from KDS

Buffers data (e.g., every 5 MB or 300 seconds)

Writes to Amazon S3
