# program designed and written by libby lebyane
# dependencies
import os
from flask import Flask
from dotenv import dotenv_values
from flask_cors import CORS, cross_origin


# controllers
import controllers.weather as WeatherController
import controllers.suggestions as SuggestionsController


# server environment variable setup
configuration = {**dotenv_values(".env")}
if configuration.get("ENVIRONMENT") == configuration.get("DEVELOPMENT_MODE"):
    # mix up the development environment configuration with the program
    configuration = {**configuration, **dotenv_values(".env.secret")}

# expose the environment variables in the whole program runtime
os.environ = {
    **os.environ,
    **configuration
}


# startup the server using the flask class
if __name__ == '__main__':
    server = Flask(__name__, static_folder="./static/",
                   static_url_path="/api/static/")
    CORS(server, resources={r"*": {"origins": "*"}})


######### SERVER ROUTES SETUP ##########
"""GET WEATHER DATA OF AN AREA"""


@server.route("/api/get_weather", methods=["GET"])
@cross_origin()
def get_weather():
    return WeatherController.get_weather()


"""GETTING AREA NAME SUGGESTIONS / AUTOCOMPLETION"""


@server.route("/api/suggestions", methods=["GET"])
@cross_origin()
def get_autocomplete_suggestions() -> str:
    return SuggestionsController.get_autocomplete_suggestions()


@server.route("/api/auto-location", methods=["GET"])
@cross_origin()
def auto_location() -> str:
    return SuggestionsController.get_location_from_ip()


######### INITIALIZE THE SERVER TO RUN ########
IS_DEBUG_MODE = os.environ.get(
    "ENVIRONMENT") == os.environ.get("DEVELOPMENT_MODE")
server.run(debug=IS_DEBUG_MODE, host="localhost")
