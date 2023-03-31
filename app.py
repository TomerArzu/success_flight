import logging

from flask import Flask
from flask_restful import Api

from resources import FlightsDataResource

logger = logging.getLogger("success_flights")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# Flask app
app = Flask(__name__)
api = Api(app)

# initializations
api.add_resource(
    FlightsDataResource,
    '/flights',
    resource_class_kwargs={
        # TODO: add an handler for post and get functions
    }
)

# run local
if __name__ == "__main__":
    app.run(port=5002, debug=True)
