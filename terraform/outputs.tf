output "ec2_lambda_arn" {
  description = "ARN of the EC2 remediation Lambda function"
  value       = aws_lambda_function.ec2_remediation.arn
}

output "rds_lambda_arn" {
  description = "ARN of the RDS remediation Lambda function"
  value       = aws_lambda_function.rds_remediation.arn
}

output "sns_topic_arn" {
  description = "ARN of the SNS notification topic"
  value       = aws_sns_topic.alerts.arn
}

output "ec2_alarm_name" {
  description = "Name of the EC2 high CPU CloudWatch alarm"
  value       = aws_cloudwatch_metric_alarm.ec2_cpu_alarm.alarm_name
}

output "ec2_status_alarm_name" {
  description = "Name of the EC2 status check CloudWatch alarm"
  value       = aws_cloudwatch_metric_alarm.ec2_status_alarm.alarm_name
}

output "rds_alarm_name" {
  description = "Name of the RDS connections CloudWatch alarm"
  value       = aws_cloudwatch_metric_alarm.rds_connection_alarm.alarm_name
}

output "lambda_iam_role_arn" {
  description = "IAM role ARN used by Lambda functions"
  value       = aws_iam_role.lambda_role.arn
}
