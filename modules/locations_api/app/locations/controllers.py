from datetime import datetime

from app.locations.models import Connection, Location
from app.locations.schemas import (
    ConnectionSchema,
    LocationSchema,
)
from app.locations.services import LocationService
from flask import request, g, Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("locations", description="Connections via geolocation.")  # noqa


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location
    
    @accepts(schema=LocationSchema)
    def post(self) -> Location:
        request.get_json()
        LocationService.push_message_into_queue(request.get_json())
        return Response(status=202)