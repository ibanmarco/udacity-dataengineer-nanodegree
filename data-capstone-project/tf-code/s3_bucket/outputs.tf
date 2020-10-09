output "etl_bucket_name" {
  value = aws_s3_bucket.etl_analysis.bucket
}

output "etl_bucket_arn" {
  value = aws_s3_bucket.etl_analysis.arn
}
