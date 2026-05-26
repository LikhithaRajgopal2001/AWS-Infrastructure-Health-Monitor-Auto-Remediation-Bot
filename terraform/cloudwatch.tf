resource "aws_cloudwatch_metric_alarm" "ec2_cpu_alarm" {
  alarm_name          = "${var.project_name}-high-cpu"
  alarm_description   = "Triggers when EC2 CPU exceeds threshold"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  statistic           = "Average"
  period              = var.alarm_period_seconds
  evaluation_periods  = var.alarm_evaluation_periods
  threshold           = var.cpu_alarm_threshold
  comparison_operator = "GreaterThanThreshold"
  treat_missing_data  = "notBreaching"

  dimensions = {
    InstanceId = var.ec2_instance_id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
  ok_actions    = [aws_sns_topic.alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "ec2_status_alarm" {
  alarm_name          = "${var.project_name}-status-check"
  alarm_description   = "Triggers when EC2 status check fails"
  metric_name         = "StatusCheckFailed"
  namespace           = "AWS/EC2"
  statistic           = "Maximum"
  period              = var.alarm_period_seconds
  evaluation_periods  = var.alarm_evaluation_periods
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching"

  dimensions = {
    InstanceId = var.ec2_instance_id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "rds_connection_alarm" {
  alarm_name          = "${var.project_name}-rds-connections"
  alarm_description   = "Triggers when RDS connection count exceeds threshold"
  metric_name         = "DatabaseConnections"
  namespace           = "AWS/RDS"
  statistic           = "Average"
  period              = var.alarm_period_seconds
  evaluation_periods  = var.alarm_evaluation_periods
  threshold           = var.rds_connection_threshold
  comparison_operator = "GreaterThanThreshold"
  treat_missing_data  = "notBreaching"

  dimensions = {
    DBInstanceIdentifier = var.rds_instance_id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
}

resource "aws_cloudwatch_log_group" "ec2_lambda_logs" {
  name              = "/aws/lambda/${var.project_name}-ec2-remediation"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "rds_lambda_logs" {
  name              = "/aws/lambda/${var.project_name}-rds-remediation"
  retention_in_days = 14
}
