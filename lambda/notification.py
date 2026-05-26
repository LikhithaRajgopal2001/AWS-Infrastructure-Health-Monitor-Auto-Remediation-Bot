import json
import os
import logging
import urllib.request
import urllib.error
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_slack_alert(instance_id: str, alarm_name: str, action: str):
    """
    Send a Slack notification via webhook URL stored in environment variable.
    Set SLACK_WEBHOOK_URL in Lambda environment variables.
    """
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

    if not webhook_url:
        logger.warning("SLACK_WEBHOOK_URL not set, skipping Slack notification.")
        return

    message = {
        "text": (
            f":rotating_light: *AWS Health Monitor Alert*\n"
            f">*Alarm:* `{alarm_name}`\n"
            f">*Resource:* `{instance_id}`\n"
            f">*Action Taken:* *{action}*\n"
            f">*Status:* :white_check_mark: Remediated automatically"
        )
    }

    try:
        data = json.dumps(message).encode("utf-8")
        req  = urllib.request.Request(
            webhook_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req) as response:
            logger.info(f"Slack notification sent. Status: {response.status}")

    except urllib.error.URLError as e:
        logger.error(f"Failed to send Slack notification: {str(e)}")


def send_sns_alert(topic_arn: str, instance_id: str, alarm_name: str, action: str):
    """
    Send a notification via AWS SNS (email/SMS).
    topic_arn comes from Terraform output or environment variable.
    """
    sns = boto3.client('sns')

    subject = f"AWS Health Monitor - Auto Remediation Triggered"
    message = (
        f"AWS Health Monitor Auto-Remediation Report\n"
        f"{'='*50}\n"
        f"Alarm Name : {alarm_name}\n"
        f"Resource   : {instance_id}\n"
        f"Action     : {action}\n"
        f"Status     : Remediated Successfully\n"
        f"{'='*50}\n"
        f"No manual action required."
    )

    try:
        sns.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
        logger.info(f"SNS notification sent to topic: {topic_arn}")

    except Exception as e:
        logger.error(f"Failed to send SNS notification: {str(e)}")
