from app.locations.models import Connection, Location  # noqa
from app.locations.schemas import ConnectionSchema, LocationSchema  # noqa


def register_routes(api, app, root="api"):
    from app.locations.controllers import api as locations_api

    api.add_namespace(locations_api, path=f"/{root}")
