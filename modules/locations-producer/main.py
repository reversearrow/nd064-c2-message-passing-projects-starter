import locations_pb2
import locations_pb2_grpc
import grpc 
import time
import json
import os

from concurrent import futures
from kafka import KafkaProducer

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

class LocationServicer(locations_pb2_grpc.LocationServiceServicer):
    def Add(self, request, context):
        request_value = {
            "person_id":request.person_id,
            "creation_time": request.creation_time,
            "latitude": request.latitude,
            "longitude": request.longitude
        }

        data = json.dumps(request_value)
        producer.send(TOPIC_NAME, data.encode('utf-8'))
        producer.flush()
        return locations_pb2.LocationMessage(**request_value)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
locations_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)