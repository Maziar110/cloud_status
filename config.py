urls = {
    "gcloud_status": "https://status.cloud.google.com/incidents.json",
}

files = {
    "gcloud_state":"./gcloud_state.txt",
}

monitor_rule = {
    "since" : 3, # Sice when should we check incidents? - in days
    "frecuency": 43200 # How many times to call Google endpoint a day - in second

}