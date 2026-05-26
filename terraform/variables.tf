variable "aws_region" {
  description = "AWS region to deploy all resources"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Prefix used to name all AWS resources"
  type        = string
  default     = "aws-health-monitor"
}

variable "ec2_instance_id" {
  description = "ID of the EC2 instance to monitor (e.g. i-0a1b2c3d4e5f67890)"
  type        = string
}

#variable "rds_instance_id" {
#  description = "ID of the RDS instance to monitor"
  #type        = string
  #default     = ""
#}

variable "cpu_alarm_threshold" {
  description = "CPU utilization % that triggers the EC2 alarm"
  type        = number
  default     = 80
}

/* variable "rds_connection_threshold" {
  description = "Number of DB connections that triggers the RDS alarm"
  type        = number
  default     = 100
} */

variable "alarm_evaluation_periods" {
  description = "Number of consecutive periods before alarm fires"
  type        = number
  default     = 2
}

variable "alarm_period_seconds" {
  description = "How often CloudWatch checks the metric (in seconds)"
  type        = number
  default     = 60
}

variable "alert_email" {
  description = "Email address to receive SNS notifications"
  type        = string
}

variable "slack_webhook_url" {
  description = "Slack incoming webhook URL for notifications"
  type        = string
  sensitive   = true
  default     = ""
}
