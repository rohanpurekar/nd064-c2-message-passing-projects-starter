from kafka import KafkaConsumer
import json

TOPIC_NAME = 'person_api'
KAFKA_SERVER = 'my-release-kafka-0.my-release-kafka-headless.default.svc.cluster.local:9092'
# location_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER, value_deserializer=lambda m: json.dumps(m.decode('utf-8')))

for message in consumer:
    print(message)
    resp=eval(json.loads((message.value)))
    print (resp)