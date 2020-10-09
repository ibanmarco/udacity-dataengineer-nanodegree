resource "aws_lambda_permission" "emr_manager" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.emr_manager.arn
  principal     = "s3.amazonaws.com"
  source_arn    = var.etl_bucket_arn
}

data "archive_file" "emr_manager_zip" {
  type        = "zip"
  source_dir  = "${path.module}/emr_manager"
  output_path = "emr_manager_lambda_function.zip"
}

resource "aws_lambda_function" "emr_manager" {
  filename         = "emr_manager_lambda_function.zip"
  function_name    = "${var.project}-EMR-manager"
  role             = aws_iam_role.lambda_emr_manager_role.arn
  handler          = "emr_manager.lambda_handler"
  source_code_hash = data.archive_file.emr_manager_zip.output_base64sha256

  memory_size = "1024"
  timeout     = "900"
  runtime     = "python3.6"

  environment {
    variables = {
      postgresql_endpoint   = var.postgresql_endpoint
      redshift_endpoint     = var.redshift_endpoint
      emr_release           = var.emr_release
      worker_count          = var.worker_count
      master_instance_type  = var.master_instance_type
      core_instance_type    = var.core_instance_type
      aws_region_name       = var.aws_region
      key_name              = "${lower(var.project)}-accesskey"
      emr_ec2_role_name     = aws_iam_role.emr_ec2_role.id
      emr_service_role_name = aws_iam_role.emr_role.id
    }
  }
}

resource "aws_s3_bucket_notification" "emr_manager" {
  bucket = var.etl_bucket_name

  lambda_function {
    lambda_function_arn = aws_lambda_function.emr_manager.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "ETL-pipelines/"
    filter_suffix       = ".py"
  }

  depends_on = [aws_lambda_permission.emr_manager]
}
