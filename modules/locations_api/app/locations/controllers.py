from datetime import datetime
from app import app
from app.locations.models import Connection, Location
from app.locations.schemas import (
    ConnectionSchema,
    LocationSchema,
)
from app.locations.services import LocationService
from flask import request, g
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List
from kafka import KafkaProducer

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("locations", description="Connections via geolocation.")  # noqa

@app.before_request
def before_request():
    # Set up a Kafka producer
    TOPIC_NAME = 'location_api'
    KAFKA_SERVER = 'my-release-kafka-0.my-release-kafka-headless.default.svc.cluster.local:9092'
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
    message=dict({'Name':'Rohan Purekar', 'status':'Alright!'})
    producer.send('test', bytes(str(message), 'utf-8'))
    producer.flush()
    # Setting Kafka to g enables us to use this
    # in other parts of our application
    g.kafka_producer = producer

@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location