import logging
from datetime import datetime, timedelta
from typing import Dict, List
from flask import g
from app import db
from app.locations.models import Connection, Location
from app.locations.schemas import ConnectionSchema, LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")




class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def push_message_into_queue(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")
        
        location_producer = g.kafka_producer
        location_producer.send(g.TOPIC_NAME, bytes(str(location), 'utf-8'))
        location_producer.flush()