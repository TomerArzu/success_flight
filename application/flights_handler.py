from application.services import success_flight_service
from application.services.success_flight_service import SuccessFlightService
from domain import Flight
from domain import Repository
from exceptions import SuccessFlightException, FlightDataNotFoundException

from logger_instance import logger


class FlightsHandler:
    def __init__(self, flights_repository, success_flight_service):
        self._flights_repository: Repository = flights_repository
        self._success_flight_service: SuccessFlightService = success_flight_service

    def handle_init_flight_doc(self):
        logger.debug("initializing flights file...")
        try:
            flights = self._flights_repository.read()

            sorted_flights, updated_flights = self._success_flight_service.calculate_success_flights(flights)

        except SuccessFlightException as ex:
            logger.debug("EXCEPTION OCCURRED DURING SETUP THE APPLICATION!")
            logger.debug(
                {
                    "error_message": ex.message,
                    "error_code": ex.error_code,
                }
            )
            raise ex
        else:
            self._flights_repository.write(sorted_flights)
            logger.debug("flights application file is ready to work")

    def handle_get_flights(self) -> list[Flight]:
        logger.debug("handle get flights")
        flights = self._flights_repository.read()

        if not flights:
            raise FlightDataNotFoundException("Flights Data was not found", "")

        return flights

    def handle_get_flight(self, flight_id: str) -> Flight:
        logger.debug("handle get flights")
        flight = self._flights_repository.read_by_id(flight_id)

        if not flight:
            raise FlightDataNotFoundException("Flight Data was not found", "")

        return flight

    def handle_post_flights(self, flights: list[Flight]):
        logger.debug("handle post flights")
        sorted_flights, updated_flights = self._success_flight_service.calculate_success_flights(flights)

        exists_flights = self._flights_repository.read()
        success_flight_service.remove_outdated_flights(exists_flights, updated_flights)
        all_flights = exists_flights + sorted_flights + updated_flights
        new_flight_list = success_flight_service.sort_flights_by_arrival(all_flights)

        self._flights_repository.write(new_flight_list)

