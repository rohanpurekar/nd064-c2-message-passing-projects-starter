from __future__ import annotations

import os
import time
import grpc
import api_items_pb2
import api_items_pb2_grpc
from concurrent import futures
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from datetime import datetime
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from geoalchemy2.functions import ST_AsText, ST_Point
from shapely.geometry.point import Point
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

base = declarative_base()

class Person(base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)


class Location(base):
    __tablename__ = "location"

    id = Column(BigInteger, primary_key=True)
    person_id = Column(Integer, ForeignKey(Person.id), nullable=False)
    coordinate = Column(Geometry("POINT"), nullable=False)
    creation_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    _wkt_shape: str = None

    @property
    def wkt_shape(self) -> str:
        # Persist binary form into readable text
        if not self._wkt_shape:
            point: Point = to_shape(self.coordinate)
            # normalize WKT returned by to_wkt() from shapely and ST_AsText() from DB
            self._wkt_shape = point.to_wkt().replace("POINT ", "ST_POINT")
        return self._wkt_shape

    @wkt_shape.setter
    def wkt_shape(self, v: str) -> None:
        self._wkt_shape = v

    def set_wkt_with_coords(self, lat: str, long: str) -> str:
        self._wkt_shape = f"ST_POINT({lat} {long})"
        return self._wkt_shape

    @hybrid_property
    def longitude(self) -> str:
        coord_text = self.wkt_shape
        return coord_text[coord_text.find(" ") + 1 : coord_text.find(")")]

    @hybrid_property
    def latitude(self) -> str:
        coord_text = self.wkt_shape
        return coord_text[coord_text.find("(") + 1 : coord_text.find(" ")]

        
class PostRequestProcessingServicer(api_items_pb2_grpc.PostRequestProcessingServiceServicer):
    def create_location(self, request, context):

        new_location = Location()
        new_location.person_id = request.person_id
        new_location.coordinate = ST_Point(request.latitude, request.longitude)
        new_location.creation_time = request.creation_time
        db_string = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        db = create_engine(db_string)
        Session = sessionmaker(bind=db)
        session = Session()
        session.add(new_location)
        session.commit()
        location_request = {
            "person_id": request.person_id,
            "creation_time": request.creation_time,
            "longitude": request.longitude,
            "latitude": request.latitude,
        }
        print(location_request)
        return api_items_pb2.LocationMessage(**location_request)

    def create_person(self, request, context):

        new_person = Person()
        new_person.first_name = request.first_name
        new_person.last_name = request.last_name
        new_person.company_name = request.company_name
        db_string = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        db = create_engine(db_string)
        Session = sessionmaker(bind=db)
        session = Session()
        query = session.query(func.max(Person.id).label("largest_num"))
        new_person.id = (query.one().largest_num) + 1
        session.add(new_person)
        session.commit()
        person_request = {
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company_name": request.company_name,
        }
        
        print(person_request)
        return api_items_pb2.PersonMessage(**person_request)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
api_items_pb2_grpc.add_PostRequestProcessingServiceServicer_to_server(PostRequestProcessingServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)