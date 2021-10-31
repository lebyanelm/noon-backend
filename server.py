# program designed and written by libby lebyane
# dependencies
import os
from flask import Flask
from dotenv import dotenv_values
from flask_cors import CORS, cross_origin


# server environment variable setup
configuration = {**dotenv_values(".env.shared")}
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


######### INITIALIZE THE SERVER TO RUN ########
IS_DEBUG_MODE = os.environ.get(
    "ENVIRONMENT") == os.environ.get("DEVELOPMENT_MODE")
server.run(debug=IS_DEBUG_MODE, host="localhost")
