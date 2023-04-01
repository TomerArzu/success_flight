from flask import Flask
from flask_restful import Api

from application import FlightsHandler
from flights_repository import FlightsRepository
from resources import FlightsResource
from resources.flights_resource import FlightResource
from services.success_flight_service import SuccessFlightService

from logger_instance import logger

# Flask app
app = Flask(__name__)
api = Api(app)

# initializations
logger.debug("initialize flight success application...")

flights_repository = FlightsRepository("data_and_mocks/airport_flight_data.csv")
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
