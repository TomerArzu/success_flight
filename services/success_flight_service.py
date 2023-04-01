import bisect
from datetime import datetime

import logger_instance
from domain.flight import Flight
from const import time_format, NUMBER_OF_SUCCESS_FLIGHTS_ALLOWED


def sort_flights_by_arrival(flights: list[Flight]):
    sorted_flights = sorted(flights, key=lambda f: f.arrival.strftime(time_format))
    return sorted_flights


def flight_duration_min(flight: Flight):
    arrival_dt = datetime.combine(datetime.min, flight.arrival)
    departure_dt = datetime.combine(datetime.min, flight.departure)

    diff_seconds = (departure_dt - arrival_dt).total_seconds()
    diff_minutes = diff_seconds / 60

    return diff_minutes


class SuccessFlightService:
    def __init__(self):
        self._successful_flights: list[Flight] = []

    def calculate_success_flights(self, flights: list[Flight]):
        logger_instance.logger.debug("calculating success flights...")
        flights_to_update = []
        sorted_flights = sort_flights_by_arrival(flights)
        sorted_arrival_times = [flight.arrival for flight in self._successful_flights]

        for flight in sorted_flights:
            if flight_duration_min(flight) >= 180:

                if len(self._successful_flights) < NUMBER_OF_SUCCESS_FLIGHTS_ALLOWED:
                    flight.success = 'success'
                    self._successful_flights.append(flight)
                    sorted_arrival_times = [flight.arrival for flight in self._successful_flights]
                else:
                    expected_index_in_successful_flights = bisect.bisect_left(sorted_arrival_times, flight.arrival)

                    if expected_index_in_successful_flights <= NUMBER_OF_SUCCESS_FLIGHTS_ALLOWED - 1:
                        extracted_flight = self._successful_flights.pop()
                        extracted_flight.success = 'fail'
                        flights_to_update.append(extracted_flight)
                        # keep the successful flight in the list with the size of NUMBER_OF_SUCCESS_FLIGHTS_ALLOWED
                        self._successful_flights = self._successful_flights[:expected_index_in_successful_flights] + [
                            flight] + self._successful_flights[expected_index_in_successful_flights:]

                        flight.success = 'success'

                        sorted_arrival_times = [flight.arrival for flight in self._successful_flights]
                    else:
                        flight.success = 'fail'
            else:
                flight.success = 'fail'
        logger_instance.logger.debug("calculated success flights done !")
        return sorted_flights, flights_to_update
