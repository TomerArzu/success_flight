from flask import Flask
from flask_restful import Api

from application import FlightsHandler
from resources import FlightsResource
from logger_instance import logger


# Flask app
app = Flask(__name__)
api = Api(app)

# initializations
logger.debug("initialize flight success application...")
flights_handler = FlightsHandler()

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
