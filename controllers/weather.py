# dependencies
import os
import urllib
import ssl
import json
from models.response import Response
from flask import request
from helpers.requests import query_string_to_dict


# controllers
"""GET WEATHER OF AN AREA"""


def get_weather():
    # read the query string sent with the request
    request_query_string = request.query_string
    request_query = query_string_to_dict(
        request_query_string.decode(encoding="ascii"))

    # get the area name from the request query
    query = request_query.get("query")

    # check if an area has been provided
    if query:
        request_url = "".join([os.environ.get("WEATHER_API_URL"), "forecast.json",
                               "?dt=2021-11-02&key=", os.environ.get("WEATHER_API_KEY"), "&q=", query])
        print("Sending request to:", request_url)

        # send the request to the weather API for the weather status
        r_context = ssl.SSLContext()
        try:
            response_json = urllib.request.urlopen(
                request_url, context=r_context).read()
            # turn the response json data into a dictionary
            response_dict = json.loads(response_json)

            # weather image is returned as 64x64 replace it with a 128x128 image size
            if response_dict.get("current"):
                response_dict["current"]["condition"]["icon"] = response_dict["current"]["condition"]["icon"].replace(
                    "64x64", "128x128")

            # send back the data to the client
            return Response(200, data=response_dict).to_json()
        except urllib.request.HTTPError as error:
            return Response(error.code, reason=error.strerror).to_json()
    else:
        return Response(400, reason="Area was not provided.").to_json()

    return Response(200).to_json()
