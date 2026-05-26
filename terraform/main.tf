provider "aws" {
  region = var.aws_region
}

resource "aws_lambda_function" "ec2_remediation" {
  filename      = "../lambda/ec2_remediation.zip"
  function_name = "${var.project_name}-ec2-remediation"
  role          = aws_iam_role.lambda_role.arn
  handler       = "ec2_remediation.lambda_handler"
  runtime       = "python3.11"
  timeout       = 30

  environment {
    variables = {
      SLACK_WEBHOOK_URL = var.slack_webhook_url
      SNS_TOPIC_ARN     = aws_sns_topic.alerts.arn
    }
  }

  depends_on = [aws_iam_role_policy.lambda_policy]
}

resource "aws_lambda_function" "rds_remediation" {
  filename      = "../lambda/rds_remediation.zip"
  function_name = "${var.project_name}-rds-remediation"
  role          = aws_iam_role.lambda_role.arn
  handler       = "rds_remediation.lambda_handler"
  runtime       = "python3.11"
  timeout       = 30

  environment {
    variables = {
      SLACK_WEBHOOK_URL = var.slack_webhook_url
      SNS_TOPIC_ARN     = aws_sns_topic.alerts.arn
    }
  }

  depends_on = [aws_iam_role_policy.lambda_policy]
}

resource "aws_cloudwatch_event_rule" "ec2_alarm_rule" {
  name        = "${var.project_name}-ec2-alarm-rule"
  description = "Trigger EC2 remediation Lambda when CloudWatch alarm fires"

  event_pattern = jsonencode({
    source      = ["aws.cloudwatch"]
    detail-type
