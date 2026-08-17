output "name_prefix" {
  value = var.name_prefix
}

output "primary_bucket_name" {
  value = aws_s3_bucket.primary.bucket
}

output "primary_bucket_arn" {
  value = aws_s3_bucket.primary.arn
}

output "replica_bucket_name" {
  value = try(aws_s3_bucket.replica[0].bucket, null)
}

output "kms_key_arn" {
  value = aws_kms_key.lab.arn
}

output "kms_key_id" {
  value = aws_kms_key.lab.key_id
}

output "settlement_writer_role_arn" {
  value = aws_iam_role.settlement_writer.arn
}

output "settlement_reader_role_arn" {
  value = aws_iam_role.settlement_reader.arn
}

output "evidence_auditor_role_arn" {
  value = aws_iam_role.evidence_auditor.arn
}

output "evidence_table_name" {
  value = aws_dynamodb_table.evidence.name
}

output "sns_topic_arn" {
  value = aws_sns_topic.alarms.arn
}

output "alarm_names" {
  value = [
    aws_cloudwatch_metric_alarm.bucket_4xx.alarm_name,
    aws_cloudwatch_metric_alarm.drill_signal.alarm_name,
  ]
}

output "drill_lambda_name" {
  value = aws_lambda_function.drill.function_name
}

output "enable_replication" {
  value = var.enable_replication
}

output "simulated_dr_guidance" {
  value = var.enable_replication ? "CRR enabled — verify replica and document promotion steps." : "CRR disabled (default). Document simulated DR: restore from versions, re-deploy Terraform in alternate region if primary region is impaired, page platform on-call, validate RTO with drill timestamps."
}
