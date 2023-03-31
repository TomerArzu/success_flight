from logger_instance import logger
import mock_pythonic_data


class FlightsHandler:
    def __init__(self):
        ...

    def handle_get_flights(self) -> list:
        logger.debug("handle_get_flights")
        flights = []
        return flights

    def handle_post_flights(self, flights: list):
        logger.debug("handle_post_flights")
        logger.debug(flights)
        return flights
