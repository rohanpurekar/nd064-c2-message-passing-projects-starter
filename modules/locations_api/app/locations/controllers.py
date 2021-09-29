from datetime import datetime

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


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        TOPIC_NAME = 'location_api'
        KAFKA_SERVER = 'my-release-kafka-0.my-release-kafka-headless.default.svc.cluster.local:9092'
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        message=dict({'Name':'Rohan Purekar', 'status':'Alright!'})
        producer.send(TOPIC_NAME, bytes(str(message), 'utf-8'))
        producer.flush()
        location: Location = LocationService.retrieve(location_id)
        return location