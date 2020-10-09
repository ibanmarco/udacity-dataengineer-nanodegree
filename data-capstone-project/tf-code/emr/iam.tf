resource "aws_iam_role" "lambda_emr_manager_role" {
  name               = "${var.project}-ETL-lambda-role"
  assume_role_policy = "${data.aws_iam_policy_document.lambda_emr_manager_role_policy_document.json}"
}

data "aws_iam_policy_document" "lambda_emr_manager_role_policy_document" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "lambda_emr_manager_policy" {
  name   = "${var.project}-ETL-lambda-policy"
  role   = "${aws_iam_role.lambda_emr_manager_role.id}"
  policy = data.aws_iam_policy_document.lambda_emr_manager_policy_document.json
}

data "aws_iam_policy_document" "lambda_emr_manager_policy_document" {
  statement {
    sid       = "CloudWatch"
    actions   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
    effect    = "Allow"
    resources = ["*"]
  }

  statement {
    sid     = "S3bucket"
    actions = ["s3:PutObject", "s3:GetObject"]
    # actions   = ["s3:PutObject", "s3:GetObject", "s3:DeleteObject"]
    effect    = "Allow"
    resources = ["${var.etl_bucket_arn}/*", "${var.etl_bucket_arn}/*"]
  }
}















# IAM role for EMR Service
resource "aws_iam_role" "emr_role" {
  name = "${var.project}-emr-role"

  assume_role_policy = <<EOF
{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "elasticmapreduce.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

}

resource "aws_iam_role_policy" "emr_role_policy" {
  name = "${var.project}-emr-policy"
  role = aws_iam_role.emr_role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Resource": "*",
            "Action": [
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:CancelSpotInstanceRequests",
                "ec2:CreateFleet",
                "ec2:CreateLaunchTemplate",
                "ec2:CreateNetworkInterface",
                "ec2:CreateSecurityGroup",
                "ec2:CreateTags",
                "ec2:DeleteLaunchTemplate",
                "ec2:DeleteNetworkInterface",
                "ec2:DeleteSecurityGroup",
                "ec2:DeleteTags",
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeAccountAttributes",
                "ec2:DescribeDhcpOptions",
                "ec2:DescribeImages",
                "ec2:DescribeInstanceStatus",
                "ec2:DescribeInstances",
                "ec2:DescribeKeyPairs",
                "ec2:DescribeLaunchTemplates",
                "ec2:DescribeNetworkAcls",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribePrefixLists",
                "ec2:DescribeRouteTables",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSpotInstanceRequests",
                "ec2:DescribeSpotPriceHistory",
                "ec2:DescribeSubnets",
                "ec2:DescribeTags",
                "ec2:DescribeVpcAttribute",
                "ec2:DescribeVpcEndpoints",
                "ec2:DescribeVpcEndpointServices",
                "ec2:DescribeVpcs",
                "ec2:DetachNetworkInterface",
                "ec2:ModifyImageAttribute",
                "ec2:ModifyInstanceAttribute",
                "ec2:RequestSpotInstances",
                "ec2:RevokeSecurityGroupEgress",
                "ec2:RunInstances",
                "ec2:TerminateInstances",
                "ec2:DeleteVolume",
                "ec2:DescribeVolumeStatus",
                "ec2:DescribeVolumes",
                "ec2:DetachVolume",
                "iam:GetRole",
                "iam:GetRolePolicy",
                "iam:ListInstanceProfiles",
                "iam:ListRolePolicies",
                "iam:PassRole",
                "s3:CreateBucket",
                "s3:Get*",
                "s3:List*",
                "sdb:BatchPutAttributes",
                "sdb:Select",
                "sqs:CreateQueue",
                "sqs:Delete*",
                "sqs:GetQueue*",
                "sqs:PurgeQueue",
                "sqs:ReceiveMessage",
                "cloudwatch:PutMetricAlarm",
                "cloudwatch:DescribeAlarms",
                "cloudwatch:DeleteAlarms",
                "application-autoscaling:RegisterScalableTarget",
                "application-autoscaling:DeregisterScalableTarget",
                "application-autoscaling:PutScalingPolicy",
                "application-autoscaling:DeleteScalingPolicy",
                "application-autoscaling:Describe*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "arn:aws:iam::*:role/aws-service-role/spot.amazonaws.com/AWSServiceRoleForEC2Spot*",
            "Condition": {
                "StringLike": {
                    "iam:AWSServiceName": "spot.amazonaws.com"
                }
            }
        }
    ]
}
EOF

}

# IAM Role for EC2 Instance Profile
resource "aws_iam_role" "emr_ec2_role" {
  name = "${var.project}-emr-role"

  assume_role_policy = <<EOF
{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

}

resource "aws_iam_instance_profile" "emr_ec2_profile" {
  name = "${var.project}-emr-ec2-profile"
  role = aws_iam_role.emr_ec2_role.name
}

resource "aws_iam_role_policy" "emr_ec2_policy" {
  name = "${var.project}-emr-ec2-policy"
  role = aws_iam_role.emr_role.id

  policy = <<EOF
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Resource": "*",
              "Action": [
                  "cloudwatch:*",
                  "dynamodb:*",
                  "ec2:Describe*",
                  "elasticmapreduce:Describe*",
                  "elasticmapreduce:ListBootstrapActions",
                  "elasticmapreduce:ListClusters",
                  "elasticmapreduce:ListInstanceGroups",
                  "elasticmapreduce:ListInstances",
                  "elasticmapreduce:ListSteps",
                  "kinesis:CreateStream",
                  "kinesis:DeleteStream",
                  "kinesis:DescribeStream",
                  "kinesis:GetRecords",
                  "kinesis:GetShardIterator",
                  "kinesis:MergeShards",
                  "kinesis:PutRecord",
                  "kinesis:SplitShard",
                  "rds:Describe*",
                  "s3:*",
                  "sdb:*",
                  "sns:*",
                  "sqs:*",
                  "glue:CreateDatabase",
                  "glue:UpdateDatabase",
                  "glue:DeleteDatabase",
                  "glue:GetDatabase",
                  "glue:GetDatabases",
                  "glue:CreateTable",
                  "glue:UpdateTable",
                  "glue:DeleteTable",
                  "glue:GetTable",
                  "glue:GetTables",
                  "glue:GetTableVersions",
                  "glue:CreatePartition",
                  "glue:BatchCreatePartition",
                  "glue:UpdatePartition",
                  "glue:DeletePartition",
                  "glue:BatchDeletePartition",
                  "glue:GetPartition",
                  "glue:GetPartitions",
                  "glue:BatchGetPartition",
                  "glue:CreateUserDefinedFunction",
                  "glue:UpdateUserDefinedFunction",
                  "glue:DeleteUserDefinedFunction",
                  "glue:GetUserDefinedFunction",
                  "glue:GetUserDefinedFunctions"
              ]
          }
      ]
  }
EOF

}
