import boto3
import json
import logging
from notification import send_slack_alert

logger = logging.getLogger()
logger.setLevel(logging.INFO)

rds = boto3.client('rds')


def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")

    try:
        # Extract DB instance ID from event
        db_instance_id = event['detail']['db-instance-id']
        alarm_name     = event['detail']['alarmName']
        state          = event['detail']['state']['value']

        logger.info(f"Alarm: {alarm_name} | DB Instance: {db_instance_id} | State: {state}")

        if state != "ALARM":
            logger.info("State is not ALARM, skipping remediation.")
            return {"status": "skipped", "reason": "not in ALARM state"}

        # Get current DB instance status
        response    = rds.describe_db_instances(DBInstanceIdentifier=db_instance_id)
        db_instance = response['DBInstances'][0]
        db_status   = db_instance['DBInstanceStatus']

        logger.info(f"Current RDS status: {db_status}")

        if db_status == 'available':
            # Reboot the RDS instance to clear connection issues
            rds.reboot_db_instance(DBInstanceIdentifier=db_instance_id)
            action = "Rebooted"
            logger.info(f"Rebooted RDS instance: {db_instance_id}")

        elif db_status == 'stopped':
            # Start the RDS instance
            rds.start_db_instance(DBInstanceIdentifier=db_instance_id)
            action = "Started"
            logger.info(f"Started RDS instance: {db_instance_id}")

        else:
            logger.info(f"RDS is in '{db_status}' state, cannot remediate.")
            return {"status": "skipped", "reason": f"RDS in {db_status} state"}

        # Send Slack notification
        send_slack_alert(
            instance_id=db_instance_id,
            alarm_name=alarm_name,
            action=f"RDS {action}"
        )

        return {
            "status"         : "remediated",
            "db_instance_id" : db_instance_id,
            "action"         : action
        }

    except Exception as e:
        logger.error(f"RDS remediation failed: {str(e)}")
        raise e
