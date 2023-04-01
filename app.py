from flask import Flask
from flask_restful import Api

from application import FlightsHandler
from flights_repository import FlightsRepository
from resources import FlightsResource
from logger_instance import logger


# Flask app
from services.success_flight_service import SuccessFlightService

app = Flask(__name__)
api = Api(app)

# initializations
logger.debug("initialize flight success application...")

flights_repository = FlightsRepository("C:\\projects\\success_flight\\airport_flight_data.csv")
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

# run local
if __name__ == "__main__":
    app.run(port=5002, debug=True)
