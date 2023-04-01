import datetime
from dataclasses import dataclass

from const import time_format


@dataclass
class Flight:
    id: str
    arrival: datetime.time
    departure: datetime.time
    success: str

    def as_serializable_dict(self):
        return {
            "flight ID": self.id,
            "Arrival": self.arrival.strftime(time_format),
            "Departure": self.departure.strftime(time_format),
            "success": self.success,
        }
