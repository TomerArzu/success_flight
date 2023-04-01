from datetime import datetime

from flask_restful import Resource
from flask import request

from domain import Flight

from const import time_format
from logger_instance import logger


class FlightResource(Resource):
    def __init__(self, **kwargs):
        self._handler = kwargs['handler']

    def get(self, flight_id: str):
        logger.debug("GET /flight/{flight_id}")
        flight = self._handler.handle_get_flight(flight_id)
        if flight is None:
            return {"message": f"flight id {flight_id} not found"}, 404

        return {"message": flight.as_serializable_dict()}, 200


class FlightsResource(Resource):
    def __init__(self, **kwargs):
        self._handler = kwargs['handler']

    def get(self):
        logger.debug("GET /flights")
        flights = self._handler.handle_get_flights()
        if not flights:
            return {"message": f"there are no flights in CSV"}, 404

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
