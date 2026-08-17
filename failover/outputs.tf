output "primary_bucket_name" {
  value = aws_s3_bucket.primary_bucket.id
}

output "replica_bucket_name" {
  value = aws_s3_bucket.replica_bucket.id
}

output "primary_lambda_function" {
  value = aws_lambda_function.primary_lambda.arn
}

output "backup_lambda_function" {
  value = aws_lambda_function.backup_lambda.arn
}
