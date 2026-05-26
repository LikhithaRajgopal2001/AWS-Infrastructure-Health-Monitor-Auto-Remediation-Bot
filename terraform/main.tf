provider "aws" {
  region = var.aws_region
}

# Lambda function
resource "aws_lambda_function" "remediation_bot" {
  filename      = "lambda/ec2_remediation.zip"
  function_name = "aws-health-monitor"
  role          = aws_iam_role.lambda_role.arn
  handler       = "ec2_remediation.lambda_handler"
  runtime       = "python3.11"
}

# CloudWatch Alarm
resource "aws_cloudwatch_metric_alarm" "cpu_alarm" {
  alarm_name          = "high-cpu-alarm"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 60
  evaluation_periods  = 2
  threshold           = 80
  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.alerts.arn]

  dimensions = {
    InstanceId = var.instance_id
  }
}
