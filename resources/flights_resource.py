from datetime import datetime

from flask_restful import Resource
from flask import request

from domain.flight import Flight
from const import time_format
from logger_instance import logger


class FlightsResource(Resource):
    def __init__(self, **kwargs):
        self._handler = kwargs['handler']

    def get(self):
        logger.debug("GET /flights")
        flights = self._handler.handle_get_flights()

        response = {
            "flights": [flight.as_serializable_dict() for flight in flights]
        }

        return response

    def post(self):
        logger.debug("POST /flights")
        flights = request.get_json()

        flights_objs = [Flight(
            id=flight["flight ID"],
            arrival=datetime.strptime(flight["Arrival"], time_format).time(),
            departure=datetime.strptime(flight["Departure"], time_format).time(),
            success=flight["success"],
        ) for flight in flights["flights"]]

        self._handler.handle_post_flights(flights_objs)
        return {"message": "flights were added"}, 200
