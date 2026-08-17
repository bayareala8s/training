# Lab 5.3: Athena Workgroup Configuration Guide

Configure via AWS Console or CLI.

## Recommended Settings

| Setting | Value | Rationale |
|---------|-------|-----------|
| Workgroup name | `cnde-analytics-dev` | Isolate student/lab spend |
| Engine version | Athena engine version 3 | Better performance |
| Query result location | `s3://{bucket}/athena-results/` | Lifecycle can expire old results |
| Bytes scanned cutoff | 10 GB (dev) / 1 GB (strict) | Prevent runaway ad hoc queries |
| CloudWatch metrics | Enabled | Track team scan trends |

## CLI Example

```bash
export BUCKET=your-datalake-bucket
export WG=cnde-analytics-dev

aws athena create-work-group \
  --name "$WG" \
  --configuration "ResultConfiguration={OutputLocation=s3://${BUCKET}/athena-results/},EnforceWorkGroupConfiguration=true,PublishCloudWatchMetricsEnabled=true" \
  --description "CNDE Module 5 analytics workgroup"

aws athena update-work-group \
  --work-group "$WG" \
  --configuration-updates "BytesScannedCutoffPerQuery=10737418240"
```

## Result Lifecycle (S3)

Add lifecycle rule on `athena-results/` prefix — expire after 7 days (Module 1 pattern).

## Analyst Policy (Document in LAB-REPORT)

1. Discovery queries must include `LIMIT 100` and single-day partition
2. Scheduled dashboards query **summary tables** only
3. No `SELECT *` on `fact_orders`
4. Escalate queries &gt; 1 GB scan to data engineering
