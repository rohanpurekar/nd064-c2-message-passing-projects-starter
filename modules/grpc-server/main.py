import os
import time
import grpc
import api_items_pb2
import api_items_pb2_grpc
from concurrent import futures
from .models import Location, Person
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

class PostRequestProcessingServicer(api_items_pb2_grpc.PostRequestProcessingServiceServicer):
    def create_location(self, request, context):
        
        new_location = Location()
        new_location.person_id = request.person_id
        new_location.creation_time = request.creation_time
        new_location.longitude = request.longitude
        new_location.latitude = request.latitude
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
        person_request = {
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company_name": request.company_name,
        }
        
        print(person_request)
        return api_items_pb2.LocationMessage(**person_request)

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