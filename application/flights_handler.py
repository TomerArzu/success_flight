import logger_instance
from logger_instance import logger
# TODO: consider to remove imports
import mock_pythonic_data
from flights_repository import FlightsRepository
from services.success_flight_service import SuccessFlightService


class FlightsHandler:
    def __init__(self, flights_repository, success_flight_service):
        # TODO: consider to remove type hint
        self._flights_repository: FlightsRepository = flights_repository
        self._success_flight_service: SuccessFlightService = success_flight_service

    def handle_init_flight_doc(self):
        flights = self._flights_repository.get_all()
        # sorted_flights = self._success_flight_service.sort_flights_by_arrival(flights)
        sorted_flights, updated_flights = self._success_flight_service.calculate_success_flights(flights)
        flights_to_write = [flight.as_serializable_dict() for flight in sorted_flights]
        self._flights_repository.write_csv(flights_to_write)
        logger_instance.logger.debug(sorted_flights)


    def handle_get_flights(self) -> list:
        logger.debug("handle_get_flights")
        flights = self._flights_repository.get_all()
        return flights

    def handle_post_flights(self, flights: list):
        logger.debug("handle_post_flights")
        logger.debug(flights)
        return flights
