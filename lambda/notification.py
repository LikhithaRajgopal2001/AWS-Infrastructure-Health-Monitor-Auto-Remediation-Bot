# lambda/notification.py

import json
import urllib.request

def send_slack_alert(instance_id, action):
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    
    message = {
        "text": f"🚨 *AWS Health Monitor Alert*\n"
                f"Instance `{instance_id}` was unhealthy\n"
                f"Action taken: *{action}*\n"
                f"Status: ✅ Remediated"
    }
    
    data = json.dumps(message).encode('utf-8')
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)
