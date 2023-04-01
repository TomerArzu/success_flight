from domain.flight import Flight
from flights_repository import CsvRepository
from logger_instance import logger
from services.success_flight_service import SuccessFlightService


def _remove_outdated_flights(exists_flights, flights_to_update):
    for flight in flights_to_update:
        exists_flights.remove(flight)


class FlightsHandler:
    def __init__(self, flights_repository, success_flight_service):
        self._flights_repository: CsvRepository = flights_repository
        self._success_flight_service: SuccessFlightService = success_flight_service

    def handle_init_flight_doc(self):
        logger.debug("initializing flights file...")
        flights = self._flights_repository.read_all()

        sorted_flights, updated_flights = self._success_flight_service.calculate_success_flights(flights)

        self._flights_repository.write_csv(sorted_flights)
        logger.debug("flights csv file is ready to work")

    def handle_get_flights(self) -> list[Flight]:
        logger.debug("handle get flights")
        flights = self._flights_repository.read_all()

        return flights

    def handle_post_flights(self, flights: list[Flight]):
        logger.debug("handle post flights")
        sorted_flights, updated_flights = self._success_flight_service.calculate_success_flights(flights)

        exists_flights = self._flights_repository.read_all()
        _remove_outdated_flights(exists_flights, updated_flights)
        all_flights = exists_flights + sorted_flights + updated_flights
        new_flight_list = self._success_flight_service.sort_flights_by_arrival(all_flights)

        self._flights_repository.write_csv(new_flight_list)

