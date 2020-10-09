####################################################################
#  Redshift
resource "aws_iam_role" "etl_redshift" {
  name               = "${var.project}-RedShift-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": [
            "arn:aws:redshift:${var.aws_region}:${var.aws_account_id}:dbuser:etl-analysis-redshift/ironman"
          ]
        }
      },
      "Principal": {
        "Service": "redshift.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "etl_redshift_access_policy_attach" {
  role       = aws_iam_role.etl_redshift.name
  policy_arn = aws_iam_policy.etl_redshift_access_policy.arn
}

resource "aws_iam_policy" "etl_redshift_access_policy" {
  name   = "${var.project}-Redshift-S3-access-policy"
  policy = data.aws_iam_policy_document.etl_redshift_access_policy.json

}

data "aws_iam_policy_document" "etl_redshift_access_policy" {

  statement {
    sid = "AllowReadingMetricsFromCloudWatch"
    actions = [
      "cloudwatch:DescribeAlarmsForMetric",
      "cloudwatch:ListMetrics",
      "cloudwatch:GetMetricStatistics",
      "cloudwatch:GetMetricData",
    "cloudwatch:Put*"]
    effect    = "Allow"
    resources = ["*"]
  }

  statement {
    sid       = "AllowS3ROFromRedShift"
    actions   = ["s3:Get*", "s3:List*"]
    effect    = "Allow"
    resources = ["*"]
  }

}

resource "aws_security_group" "redshift_sg" {
  name        = "${var.project}-redshift-sg"
  description = "SG for allowing access to Redshift"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = "5439"
    to_port     = "5439"
    protocol    = "tcp"
    description = "Redshift access from private subnets"
    cidr_blocks = ["${var.bastion_private_ip}/32"]
  }
}

resource "random_string" "redshift_dbpassword" {
  length      = 15
  min_upper   = 2
  min_lower   = 2
  min_numeric = 2
  special     = false
}

resource "aws_ssm_parameter" "redshift_dbpassword" {
  name      = "${var.project}-redshift_dbpassword"
  value     = random_string.redshift_dbpassword.result
  type      = "SecureString"
  key_id    = var.kms_arn
  overwrite = "true"
}

resource "aws_redshift_cluster" "redshift" {
  cluster_identifier     = "${lower(var.project)}-redshift"
  database_name          = var.dbname
  master_username        = var.db_master_username
  master_password        = random_string.redshift_dbpassword.result
  node_type              = var.redshift_node_type
  cluster_type           = var.redshift_cluster_type
  number_of_nodes        = var.redshift_nodes
  iam_roles              = [aws_iam_role.etl_redshift.arn]
  vpc_security_group_ids = [aws_security_group.redshift_sg.id]
  publicly_accessible    = var.redshift_publicly_accessible
  skip_final_snapshot    = var.redshift_skip_final_snapshot
}
