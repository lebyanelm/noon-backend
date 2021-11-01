# depedencies
import urllib
import os
import ssl
import json
import helpers.requests
from models.response import Response
from flask import request


"""Automatically suggest areas that match the name of the query"""


def get_autocomplete_suggestions() -> str:
    # get the name of the area to find autocompletion for
    request_query = helpers.requests.query_string_to_dict(
        request.query_string.decode("ascii"))
    query = request_query.get("query")

    if query:
        # build the url to send to the weather API to get results relevent to them, instead of using google places.
        request_url = "".join([os.environ.get(
            "WEATHER_API_URL"), "search.json?key=", os.environ.get("WEATHER_API_KEY"), "&q=", query])

        print("Getting suggestions from:", request_url)

        # send the request to the api url
        try:
            request_context = ssl.SSLContext()
            response_data = urllib.request.urlopen(
                request_url, context=request_context).read()

            # convert the data to a python accessible dictionary object
            try:
                response_data = json.loads(response_data)

                return Response(200, data=response_data).to_json()
            except Exception as e:
                return Response(500).to_json()
        except urllib.request.HTTPError as e:
            return Response(e.code).to_json()
        return Response(500).to_json()
    else:
        return Response(400).to_json()
