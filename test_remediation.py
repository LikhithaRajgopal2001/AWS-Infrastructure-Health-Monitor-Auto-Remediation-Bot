import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add lambda folder to path so we can import the functions
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambda'))


# -------------------------------------------------------
# EC2 Remediation Tests
# -------------------------------------------------------
class TestEC2Remediation(unittest.TestCase):

    def _make_event(self, instance_id, alarm_name, state="ALARM"):
        """Helper to build a fake CloudWatch alarm event."""
        return {
            "detail": {
                "instance-id": instance_id,
                "alarmName"  : alarm_name,
                "state"      : {"value": state}
            }
        }

    @patch("ec2_remediation.send_slack_alert")
    @patch("ec2_remediation.ec2")
    def test_running_instance_is_rebooted(self, mock_ec2, mock_slack):
        """Running instance should be rebooted when alarm fires."""
        mock_ec2.describe_instances.return_value = {
            "Reservations": [{"Instances": [{"State": {"Name": "running"}}]}]
        }

        from ec2_remediation import lambda_handler
        event  = self._make_event("i-abc123", "aws-health-monitor-high-cpu")
        result = lambda_handler(event, {})

        mock_ec2.reboot_instances.assert_called_once_with(InstanceIds=["i-abc123"])
        self.assertEqual(result["status"], "remediated")
        self.assertEqual(result["action"], "Rebooted")

    @patch("ec2_remediation.send_slack_alert")
    @patch("ec2_remediation.ec2")
    def test_stopped_instance_is_started(self, mock_ec2, mock_slack):
        """Stopped instance should be started when alarm fires."""
        mock_ec2.describe_instances.return_value = {
            "Reservations": [{"Instances": [{"State": {"Name": "stopped"}}]}]
        }

        from ec2_remediation import lambda_handler
        event  = self._make_event("i-abc123", "aws-health-monitor-status-check")
        result = lambda_handler(event, {})

        mock_ec2.start_instances.assert_called_once_with(InstanceIds=["i-abc123"])
        self.assertEqual(result["status"], "remediated")
        self.assertEqual(result["action"], "Started")

    @patch("ec2_remediation.ec2")
    def test_non_alarm_state_is_skipped(self, mock_ec2):
        """Events that are not ALARM state should be skipped."""
        from ec2_remediation import lambda_handler
        event  = self._make_event("i-abc123", "aws-health-monitor-high-cpu", state="OK")
        result = lambda_handler(event, {})

        mock_ec2.reboot_instances.assert_not_called()
        self.assertEqual(result["status"], "skipped")

    @patch("ec2_remediation.ec2")
    def test_pending_instance_is_skipped(self, mock_ec2):
        """Instance in pending state should not be touched."""
        mock_ec2.describe_instances.return_value = {
            "Reservations": [{"Instances": [{"State": {"Name": "pending"}}]}]
        }

        from ec2_remediation import lambda_handler
        event  = self._make_event("i-abc123", "aws-health-monitor-high-cpu")
        result = lambda_handler(event, {})

        mock_ec2.reboot_instances.assert_not_called()
        self.assertEqual(result["status"], "skipped")


# -------------------------------------------------------
# RDS Remediation Tests
# -------------------------------------------------------
class TestRDSRemediation(unittest.TestCase):

    def _make_event(self, db_instance_id, alarm_name, state="ALARM"):
        return {
            "detail": {
                "db-instance-id": db_instance_id,
                "alarmName"     : alarm_name,
                "state"         : {"value": state}
            }
        }

    @patch("rds_remediation.send_slack_alert")
    @patch("rds_remediation.rds")
    def test_available_rds_is_rebooted(self, mock_rds, mock_slack):
        """Available RDS instance should be rebooted when alarm fires."""
        mock_rds.describe_db_instances.return_value = {
            "DBInstances": [{"DBInstanceStatus": "available"}]
        }

        from rds_remediation import lambda_handler
        event  = self._make_event("mydb", "aws-health-monitor-rds-connections")
        result = lambda_handler(event, {})

        mock_rds.reboot_db_instance.assert_called_once_with(DBInstanceIdentifier="mydb")
        self.assertEqual(result["status"], "remediated")

    @patch("rds_remediation.rds")
    def test_non_alarm_state_is_skipped(self, mock_rds):
        """Non-ALARM events should be skipped for RDS too."""
        from rds_remediation import lambda_handler
        event  = self._make_event("mydb", "aws-health-monitor-rds-connections", state="OK")
        result = lambda_handler(event, {})

        mock_rds.reboot_db_instance.assert_not_called()
        self.assertEqual(result["status"], "skipped")


# -------------------------------------------------------
# Notification Tests
# -------------------------------------------------------
class TestNotification(unittest.TestCase):

    @patch.dict(os.environ, {"SLACK_WEBHOOK_URL": ""})
    def test_slack_skipped_when_no_webhook(self):
        """Slack alert should be skipped when webhook URL is not set."""
        from notification import send_slack_alert
        # Should not raise any exception
        send_slack_alert("i-abc123", "test-alarm", "Rebooted")

    @patch("notification.urllib.request.urlopen")
    @patch.dict(os.environ, {"SLACK_WEBHOOK_URL": "https://hooks.slack.com/fake"})
    def test_slack_sends_message(self, mock_urlopen):
        """Slack alert should call urlopen when webhook is set."""
        mock_response      = MagicMock()
        mock_response.status = 200
        mock_urlopen.return_value.__enter__ = lambda s: mock_response
        mock_urlopen.return_value.__exit__  = MagicMock(return_value=False)

        from notification import send_slack_alert
        send_slack_alert("i-abc123", "test-alarm", "Rebooted")

        mock_urlopen.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
