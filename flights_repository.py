import csv
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TypeVar, Optional

import logger_instance
from domain.flight import Flight
from const import time_format

T = TypeVar("T")


class Repository(ABC):

    @abstractmethod
    def read(self) -> list[T]:
        ...

    @abstractmethod
    def read_by_id(self, line_id: T) -> T | None:
        ...

    @abstractmethod
    def write(self, data: list[T] | T):
        ...


class FlightsRepository(Repository):
    def __init__(self, path_to_file):
        self._path_to_file = path_to_file
        self._fieldnames = ["flight ID", "Arrival", "Departure", "success"]

    def read(self) -> list[Flight]:
        logger_instance.logger.debug("retrieving all data from csv...")
        flights = []

        try:
            with open(self._path_to_file, mode='r') as csv_file:
                logger_instance.logger.debug(f"csv file opened {self._path_to_file}")
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
            logger_instance.logger.debug("error occurred while retrieving flights data from csv")
            logger_instance.logger.debug(te)
        except KeyError as ke:
            logger_instance.logger.debug("invalid field name, check csv format")
            logger_instance.logger.debug(ke)

        return flights

    def read_by_id(self, line_id: str) -> Flight | None:
        logger_instance.logger.debug(f"retrieving flight {line_id} data from csv...")
        flight = None

        try:
            with open(self._path_to_file, mode='r') as csv_file:
                logger_instance.logger.debug(f"csv file opened {self._path_to_file}")
                csv_reader = csv.DictReader(csv_file, skipinitialspace=True)

                for line in csv_reader:
                    if line["flight ID"] == line_id:
                        flight = Flight(
                            id=line["flight ID"],
                            arrival=datetime.strptime(line["Arrival"], time_format).time(),
                            departure=datetime.strptime(line["Departure"], time_format).time(),
                            success=line["success"],
                        )

        except TypeError as te:
            logger_instance.logger.debug("error occurred while retrieving flights data from csv")
            logger_instance.logger.debug(te)
        except KeyError as ke:
            logger_instance.logger.debug("invalid field name, check csv format")
            logger_instance.logger.debug(ke)

        return flight

    def write(self, data: list[Flight] | Flight):
        logger_instance.logger.debug("writing new data to csv file...")

        with open(self._path_to_file, mode='w', newline="\n") as csv_file:
            logger_instance.logger.debug(f"csv file opened {self._path_to_file}")
            writer = csv.DictWriter(csv_file, fieldnames=self._fieldnames)
            writer.writeheader()

            for line in data:
                writer.writerow(line.as_serializable_dict())

        logger_instance.logger.debug("new data has been saved !")
