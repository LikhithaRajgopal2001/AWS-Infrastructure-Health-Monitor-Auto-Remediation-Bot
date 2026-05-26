resource "aws_iam_role" "lambda_role" {
  name        = "${var.project_name}-lambda-role"
  description = "IAM role for AWS Health Monitor Lambda functions"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["ec2:DescribeInstances", "ec2:RebootInstances", "ec2:StartInstances", "ec2:StopInstances"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["rds:DescribeDBInstances", "rds:RebootDBInstance", "rds:StartDBInstance", "rds:StopDBInstance"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["sns:Publish"]
        Resource = aws_sns_topic.alerts.arn
      },
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect   = "Allow"
        Action   = ["cloudwatch:DescribeAlarms", "cloudwatch:GetMetricStatistics"]
        Resource = "*"
      }
    ]
  })
}
