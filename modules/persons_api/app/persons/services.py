import logging
from datetime import datetime, timedelta

from typing import Dict, List

from app import db
from app.persons.models import Person
from app.persons.schemas import PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from kafka import KafkaProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")




class PersonService:
    @staticmethod
    def push_person_into_queue(person: Dict) -> Person:
        validation_results: Dict = PersonSchema().validate(persons)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        TOPIC_NAME = 'person_api'
        KAFKA_SERVER = 'my-release-kafka-0.my-release-kafka-headless.default.svc.cluster.local:9092'
        location_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        location_producer.send(TOPIC_NAME, bytes(str(person), 'utf-8'))
        location_producer.flush()
        # new_person = Person()
        # new_person.first_name = person["first_name"]
        # new_person.last_name = person["last_name"]
        # new_person.company_name = person["company_name"]

        # db.session.add(new_person)
        # db.session.commit()

        # return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()