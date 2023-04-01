import csv
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TypeVar, Optional

import logger_instance
from Domain.flight import Flight
from const import time_format

T = TypeVar("T")


class CsvRepository(ABC):
    # CRUD - CREATE, READ, UPDATE, DELETE
    @abstractmethod
    def get_all(self) -> list[T]:
        ...

    @abstractmethod
    def get(self, row_id: T) -> Optional[T]:
        ...

    @abstractmethod
    def update_lines(self, data: list[T] | T) -> bool:
        ...

    @abstractmethod
    def append_lines(self, data: list[T] | T) -> bool:
        ...

    @abstractmethod
    def delete(self, data: T) -> bool:
        ...


class FlightsRepository(CsvRepository):
    def __init__(self, full_path):
        self._full_path = full_path
        self._fieldnames = ["flight ID", "Arrival", "Departure", "success"]
        # self._file_cursor = None

    def get_all(self) -> list[Flight]:
        flights = []
        try:
            with open(self._full_path, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file, skipinitialspace=True)
                for line in csv_reader:
                    flights.append(
                        Flight(
                            id=line["flight ID"],
                            arrival=datetime.strptime(line["Arrival"], time_format).time(),
                            departure=datetime.strptime(line["Departure"], time_format).time(),
                            success=line["success"],
                        )
                    )
        except TypeError as te:
            logger_instance.logger.debug(te)
        return flights

    def get(self, row_id: Flight) -> Optional[Flight]:
        pass

    def write_csv(self, data: list[Flight] | Flight):
        with open("airport_flight_data_filled_sorted.csv", mode='w', newline="\n") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self._fieldnames)
            writer.writeheader()

            for line in data:
                writer.writerow(line)

    def update_lines(self, data: list[Flight] | Flight) -> bool:
        pass

    def append_lines(self, data: list[Flight] | Flight) -> bool:
        pass

    def delete(self, data: Flight) -> bool:
        pass
