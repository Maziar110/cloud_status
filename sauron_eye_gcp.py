"""
To monitor Gcloud related status
"""
import requests
import config
import datetime
import files
from os import path
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')

class Gcloud:
    gcloud_state_file = config.files["gcloud_state"]

    def gcp_stat_handler(self):
        gcp_events = self.status_monitor_api()
        if gcp_events:
            events = self.events_analyzer(gcp_events)
            if len(events)>0:
                return events
            else:
                logging.info("The Analyzed events were already raised")
                return None
        else:
            logging.info("No new event in GCP")
            return None

    def status_monitor_api(self) -> dict:
        current_time = datetime.datetime.now()
        days_ago = current_time - datetime.timedelta(days=config.monitor_rule["since"])
        url = config.urls["gcloud_status"]
        gcloud_events = {}
        try:
            resp = requests.get(url=url)
            if 200 <= resp.status_code < 300:
                logging.info(f"Total events: {len(resp.json())}")
                for event in resp.json():
                    # Check event's to gather latest ones
                    if datetime.datetime.strptime(event["begin"], '%Y-%m-%dT%H:%M:%S+00:00') > days_ago:
                        id = event["id"]
                        gcloud_events[id] = {}
                        gcloud_events[id]["begin"] = event['begin']
                        gcloud_events[id]['desc'] = event['external_desc']
                logging.info("Checking events...")
                return (gcloud_events)
                
        except Exception as e:
            logging.error("Error in Sauron EYE: ", e)
            return None
    
    def events_analyzer(self, gcloud_events: dict) -> list:
        new_events = [] # New incidents compared to state file
        new_events_ids = []
        has_equal_state = False
        if path.exists(self.gcloud_state_file):
            file = files.Read()
            states = file.read_state(self.gcloud_state_file)
            if states and len(states) > 0:
                logging.info("Comparing events...")
                for event in gcloud_events: # Compares events' IDs with stat to see if there's a new event
                    for state in states: 
                        # logging.info(f"comparing if {event} is equal to {state}") # Good for debuging search part
                        if event == state.strip('\n'):
                            has_equal_state = True
                            pass
                    if not has_equal_state:
                        logging.info(f"New state ID detected: {event}, old state was: {state}!")
                        new_events.append(gcloud_events[event]) 
                        new_events_ids.append(event)
                        file_write = files.Write() 
                        file_write.write_state(new_events_ids, self.gcloud_state_file)
                return new_events
            else:
                try:
                    logging.info(f"There is a file for states but it looks empty, going to delete {self.gcloud_state_file}")
                    os.remove(self.gcloud_state_file)
                    self.status_monitor_api()
                except Exception as e:
                    logging.error(f"Error while removing {self.gcloud_state_file}", e)
                    return None

        else:
            logging.info("Creating new file to update states...")
            file = files.Write() 
            for event in gcloud_events:
                    new_events.append(gcloud_events[event])
                    new_events_ids.append(event)
            file.write_state(new_events_ids, self.gcloud_state_file)
            logging.info(f"There were {len(new_events)} events")
            return new_events
