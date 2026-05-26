# lambda/ec2_remediation.py

import boto3
import json

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Get instance ID from the CloudWatch alarm event
    instance_id = event['detail']['instance-id']
    
    print(f"Unhealthy instance detected: {instance_id}")
    
    # Auto remediation — reboot the instance
    ec2.reboot_instances(InstanceIds=[instance_id])
    
    print(f"Rebooted instance: {instance_id}")
    
    return {
        "status": "remediated",
        "instance": instance_id
    }
    
# Update ec2_remediation.py to call notification
from notification import send_slack_alert

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    instance_id = event['detail']['instance-id']
    
    ec2.reboot_instances(InstanceIds=[instance_id])
    
    # Send Slack alert
    send_slack_alert(instance_id, "EC2 Reboot")      # ← Add this
    
    return {"status": "remediated", "instance": instance_id}
