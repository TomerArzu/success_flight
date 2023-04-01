import csv
from datetime import datetime

from domain import Repository
from domain import Flight

import logger_instance
from const import time_format
from exceptions import DataSourceNotFoundException, DataSourceParsingException, DataSourceLineHeadersException


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
        except FileNotFoundError as fnfe:
            raise DataSourceNotFoundException(f"Could not find data source in the provided path `{self._path_to_file}`"
                                              f", please check if data source exists", fnfe) from fnfe
        except TypeError as te:
            raise DataSourceParsingException(f"Could not parse provided csv. "
                                             f"During parsing, unexpected type of data was found", te) from te
        except KeyError as ke:
            raise DataSourceLineHeadersException(f"Wrong field in csv file. "
                                                 f"field name {ke.args[0]} is not one of defiled fields"
                                                 f"Fields name must be: {self._path_to_file}", ke) from ke
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
        except FileNotFoundError as fnfe:
            raise DataSourceNotFoundException(f"Could not find data source in the provided path `{self._path_to_file}`"
                                              f", please check if data source exists", fnfe) from fnfe
        except TypeError as te:
            raise DataSourceParsingException(f"Could not parse provided csv. "
                                             f"During parsing, unexpected type of data was found", te) from te
        except KeyError as ke:
            raise DataSourceLineHeadersException(f"Wrong field in csv file. "
                                                 f"field name {ke.args[0]} is not one of defiled fields"
                                                 f"Fields name must be: {self._path_to_file}", ke) from ke

        return flight

    def write(self, data: list[Flight] | Flight):
        logger_instance.logger.debug("writing new data to csv file...")

        try:
            with open(self._path_to_file, mode='w', newline="\n") as csv_file:
                logger_instance.logger.debug(f"csv file opened {self._path_to_file}")
                writer = csv.DictWriter(csv_file, fieldnames=self._fieldnames)
                writer.writeheader()

                for line in data:
                    writer.writerow(line.as_serializable_dict())
                logger_instance.logger.debug("new data has been saved !")
        except FileNotFoundError as fnfe:
            raise DataSourceNotFoundException(
                f"Could not find data source in the provided path `{self._path_to_file}`"
                f", please check if data source exists", fnfe) from fnfe
