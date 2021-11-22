import json
import requests
import os
from datetime import datetime
from kafka import KafkaConsumer

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]
LOCATIONS_URL = os.environ["LOCATIONS_URL"]

consumer = KafkaConsumer(TOPIC_NAME,bootstrap_servers=KAFKA_SERVER)

print("starting consumer")

for message in consumer:
    data = json.loads(message.value.decode())
    data["creation_time"] = datetime.utcfromtimestamp(data["creation_time"]).strftime('%Y-%m-%d %H:%M:%S')
    r = requests.post(LOCATIONS_URL,  data=json.dumps(data), headers={"Content-Type": "application/json"})