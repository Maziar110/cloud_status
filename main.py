import sauron_eye_gcp
import time
import monitors
import logging
import config


logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')


# Monitors gcloud status page to find issues
gcm = sauron_eye_gcp.Gcloud()
while 1:
    events = gcm.gcp_stat_handler()
    logging.info(f"List of events: \n '{events}'")
    if events and len(events) > 0:
        alert = monitors.Slack()
        for event in events:
            alert_message = f"{event['desc']} started at {event['begin']}"
            alert_body = {
                "body" : alert_message,
                "title" : "Gcloud unstability detected",
                "name" : "DevOps Eys"
            }
            raised_in_slack = alert.drop_alert_to_channel(alert_body)
            if not raised_in_slack:
                logging.error(f"Error to send alert into slack channel- body: {alert_body}")
    time.sleep(config.monitor_rule["frecuency"])