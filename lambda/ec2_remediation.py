import boto3
import json
import logging
from notification import send_slack_alert

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client('ec2')


def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")

    try:
        # Extract instance ID from CloudWatch alarm event
        instance_id = event['detail']['instance-id']
        alarm_name  = event['detail']['alarmName']
        state       = event['detail']['state']['value']

        logger.info(f"Alarm: {alarm_name} | Instance: {instance_id} | State: {state}")

        if state != "ALARM":
            logger.info("State is not ALARM, skipping remediation.")
            return {"status": "skipped", "reason": "not in ALARM state"}

        # Check current instance state
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance  = response['Reservations'][0]['Instances'][0]
        current_state = instance['State']['Name']

        logger.info(f"Current EC2 state: {current_state}")

        if current_state == 'running':
            # Reboot the instance
            ec2.reboot_instances(InstanceIds=[instance_id])
            action = "Rebooted"
            logger.info(f"Rebooted instance: {instance_id}")

        elif current_state == 'stopped':
            # Start the instance if it is stopped
            ec2.start_instances(InstanceIds=[instance_id])
            action = "Started"
            logger.info(f"Started instance: {instance_id}")

        else:
            logger.info(f"Instance is in '{current_state}' state, cannot remediate.")
            return {"status": "skipped", "reason": f"instance in {current_state} state"}

        # Send Slack notification
        send_slack_alert(
            instance_id=instance_id,
            alarm_name=alarm_name,
            action=action
        )

        return {
            "status"     : "remediated",
            "instance_id": instance_id,
            "action"     : action
        }

    except Exception as e:
        logger.error(f"Remediation failed: {str(e)}")
        raise e
