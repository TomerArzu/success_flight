import bisect
from datetime import datetime

from Domain.flight import Flight
from const import time_format, NUMBER_OF_SUCCESS_FLIGHTS_ALLOWED


class SuccessFlightService:
    def __init__(self):
        self._successful_flights: list[Flight] = []

    def sort_flights_by_arrival(self, flights: list[Flight]):
        sorted_flights = sorted(flights, key=lambda f: f.arrival.strftime(time_format))
        return sorted_flights

    def calculate_success_flights(self, flights: list[Flight]):
        flights_to_update = []
        sorted_flights = self.sort_flights_by_arrival(flights)
        sorted_arrival_times = [flight.arrival for flight in self._successful_flights]
        for flight in sorted_flights:
            if self.flight_duration_min(flight) >= 180:
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
                        self._successful_flights = self._successful_flights[:expected_index_in_successful_flights] + [
                            flight] + self._successful_flights[expected_index_in_successful_flights:]
                        sorted_arrival_times = [flight.arrival for flight in self._successful_flights]
                    else:
                        flight.success = 'fail'
            else:
                flight.success = 'fail'
        return sorted_flights, flights_to_update


    def flight_duration_min(self, flight: Flight):
        arrival_dt = datetime.combine(datetime.min, flight.arrival)
        departure_dt = datetime.combine(datetime.min, flight.departure)

        diff_seconds = (departure_dt - arrival_dt).total_seconds()
        diff_minutes = diff_seconds / 60

        return diff_minutes
