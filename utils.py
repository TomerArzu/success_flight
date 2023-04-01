# import json
# from Domain.flight import Flight
# from const import time_format
#
#
# class FlightEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Flight):
#             return {"flight ID": obj.id, "Arrival": obj.arrival.strftime(time_format),
#                     "Departure": obj.departure.strftime(time_format), "success": obj.success}
#         return super().default(obj)
