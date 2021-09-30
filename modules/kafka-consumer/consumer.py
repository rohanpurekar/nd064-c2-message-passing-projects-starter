import grpc
import api_items_pb2
import api_items_pb2_grpc
from kafka import KafkaConsumer
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kafka-consumer")

TOPIC_NAME = 'person_api'
KAFKA_SERVER = 'my-release-kafka-0.my-release-kafka-headless.default.svc.cluster.local:9092'
# location_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER], value_deserializer=lambda m: json.dumps(m.decode('utf-8')))


# channel = grpc.insecure_channel("grpc-server.default.svc.cluster.local:5005")
# stub = api_items_pb2_grpc.PostRequestProcessingServiceStub(channel)

for message in consumer:
    json_message=eval(json.loads((message.value)))
    
    if "person_id" in json_message:
        logger.info(json_message["person_id"])
    else:
        logger.info(json_message.person_id)
        # item = api_items_pb2.LocationMessage(
        #     person_id=json_message.person
        # )
        #grpc 
    # elif "first_name" in json_message:
        #grpc
    