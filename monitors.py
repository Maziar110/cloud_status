"""
This Module is a place for integrating channels and monitors
"""
from dotenv import load_dotenv
import os 
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')

class Slack:
    load_dotenv("./.env")
    slack_webhook =  os.getenv('SLACK_WEBHOOK')
    if not slack_webhook:
        raise Exception("No Slack webhook is provided")


    def drop_alert_to_channel(self, alert_text: dict) -> bool:
        """
        Gets a dictionary with: name, title and body and a name to display as username for each alert
        """
        url = self.slack_webhook
        if alert_text:
            logging.info("Sending events to Slack channel...")
            data = {
                        "username": alert_text["name"],
                        "attachments": [
                            {
                                "color": "#9733EE",
                                "fields": [
                                    {
                                        "title": alert_text["title"],
                                        "value": alert_text["body"],
                                        "short": "false",
                                    }
                                            ]
                            }
                        ]
                     }
            header = {'Content-Type': "application/json"}
            try:
                resp = requests.post(url=url,json=data, headers=header )
                if resp.status_code == 200:
                    logging.info("Event sent to slack channel")
                    return True
                else:
                    return False
            except Exception as e:
                logging.error(f"Failed to send event to slack with status {resp.status_code}, error: ", e)
        else:
            logging.error(f"The Content for slack channel is not correct, failed with status {resp.status_code}")
            

        



