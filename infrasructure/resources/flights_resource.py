from datetime import datetime

from flask_restful import Resource
from flask import request

from domain import Flight

from const import time_format
from exceptions import SuccessFlightException
from logger_instance import logger


class FlightResource(Resource):
    def __init__(self, **kwargs):
        self._handler = kwargs['handler']

    def get(self, flight_id: str):
        logger.debug("GET /flight/{flight_id}")

        try:
            flight = self._handler.handle_get_flight(flight_id)

        except SuccessFlightException as ex:
            logger.debug(ex.exception_message)
            response = {
                           "error_code": ex.error_code,
                           "status_code": ex.http_status_code,
                           "error_message": ex.message,
                       }, ex.http_status_code

        else:
            response = {"message": flight.as_serializable_dict()}, 200

        return response


class FlightsResource(Resource):
    def __init__(self, **kwargs):
        self._handler = kwargs['handler']

    def get(self):
        logger.debug("GET /flights")

        try:
            flights = self._handler.handle_get_flights()

        except SuccessFlightException as ex:
            logger.debug(ex.exception_message)
            response = {
                           "error_code": ex.error_code,
                           "status_code": ex.http_status_code,
                           "error_message": ex.message,
                       }, ex.http_status_code
        else:
            response = {
                "message": [flight.as_serializable_dict() for flight in flights]
            }

        return response

    def post(self):
        logger.debug("POST /flights")
        flights = request.get_json()
        response = {"message": "flights were added"}, 200

        try:
            flights_objs = [Flight(
                id=flight["flight ID"],
                arrival=datetime.strptime(flight["Arrival"], time_format).time(),
                departure=datetime.strptime(flight["Departure"], time_format).time(),
                success=flight.get("success", ""),
            ) for flight in flights["flights"]]

            self._handler.handle_post_flights(flights_objs)

        except (KeyError, ValueError) as ke:
            response = {
                           "error_message": "The request body is not valid",
                           "error_code": "BAD_REQUEST.INVALID_BODY_MESSAGE"
                       }, 400
            logger.debug(response)
        except SuccessFlightException as ex:
            logger.debug(ex.exception_message)
            response = {
                           "error_code": ex.error_code,
                           "status_code": ex.http_status_code,
                           "error_message": ex.message,
                       }, ex.http_status_code

        return response
