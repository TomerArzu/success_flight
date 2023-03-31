from flask_restful import Resource
from flask import request

from application import FlightsHandler
from logger_instance import logger


class FlightsResource(Resource):
    def __init__(self, **kwargs):
        # TODO: consider to remove type hint
        self._handler: FlightsHandler = kwargs['handler']

    def get(self):
        logger.debug("GET /flights")
        flights = self._handler.handle_get_flights()
        response = {
            "flights": flights
        }
        return response

    def post(self):
        logger.debug("POST /flights")
        flights = request.get_json()
        response = self._handler.handle_post_flights(flights)
        return response, 200
