from flask import Flask
from flask_restful import Api

from application import FlightsHandler
from application import SuccessFlightService
from const import DATA_SOURCE_LOCATION

from infrasructure.repositories.flights_repository import FlightsRepository
from infrasructure.resources import FlightsResource
from infrasructure.resources.flights_resource import FlightResource

from logger_instance import logger

# Flask app
app = Flask(__name__)
api = Api(app)

# initializations
logger.debug("initialize flight success application...")

flights_repository = FlightsRepository(DATA_SOURCE_LOCATION)
success_flight_service = SuccessFlightService()
flights_handler = FlightsHandler(
    flights_repository=flights_repository,
    success_flight_service=success_flight_service
)

flights_handler.handle_init_flight_doc()

api.add_resource(
    FlightsResource,
    '/flights',
    resource_class_kwargs={
        "handler": flights_handler
    }
)
api.add_resource(
    FlightResource,
    '/flight/<string:flight_id>',
    resource_class_kwargs={
        "handler": flights_handler
    }
)
logger.debug("success flights application ready to use")

# run local
if __name__ == "__main__":
    app.run(port=5002, debug=True)
