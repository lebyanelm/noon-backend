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

    # to save number of calls with the api service, don't send empty requests
    if query or len(query) != 0:
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
        if query != None:
            # send an empty list since no area name was provided
            return Response(200, data=[]).to_json()
        else:
            # let the client know that a parameter or format of the request is incorrect
            return Response(400).to_json()


"""GETS USER LOCATION FROM A PROVIDED IP ADDRESS"""


def get_location_from_ip():
    # format the request string
    ipstack_api_uri = os.environ.get("IPSTACK_API_URL").replace(
        "ip_address", "105.12.0.105")

    # attempt to send the request to the API
    try:
        response_body = urllib.request.urlopen(ipstack_api_uri).read()
        # parse the json data returned back
        if response_body:
            response_body = json.loads(response_body)
            # return the location as coordinates to remove confusion with different return types
            coordinates = dict(latitude=response_body.get(
                "latitude"), longitude=response_body.get("longitude"))

            # get the details of that place using Google Places API
            formatted_address = _get_formatted_address(coordinates)
            if len(formatted_address) == 0:
                country_name = response_body.get("country_name")
                city_name = response_body.get("city")

                formatted_address = []
                if city_name:
                    formatted_address.append(city_name)
                if country_name:
                    formatted_address.append(country_name)
                formatted_address = ", ".join(formatted_address)

            return Response(200, data=dict(coordinates=coordinates, formatted_address=formatted_address)).to_json()
        else:
            return Response(404).to_json()
    except urllib.request.HTTPError as e:
        return Response(e.code).to_json()

    return Response(200).to_json()


"""CONVERT COORDINATES TO AN ADDRESS USING GOOGLE GEOLOCATION API TO GET PLACE ID"""


def _get_formatted_address(coordinates: dict) -> str:
    # formate the address uri of the api endpoint to get the place_id of the area
    str_coordinates = ",".join(
        [str(coordinates["latitude"]), str(coordinates["longitude"])])
    goecoding_api_url = os.environ.get(
        "GEOCODING_API_URL").replace("LAT_LNG", str_coordinates)

    # attempt sending the geocoding request
    try:
        geocoding_body = urllib.request.urlopen(
            goecoding_api_url, context=ssl.SSLContext()).read()
        if geocoding_body:
            geocoding_body = json.loads(geocoding_body)
            if geocoding_body.get("status") == "OK" and len(geocoding_body.get("results")) != 0:
                formatted_address = geocoding_body.get(
                    "results")[0]["formatted_address"]
                return formatted_address
            else:
                return str()
        else:
            # if something goes wrong return an empty string
            return str()
    except urllib.request.HTTPError as e:
        return str()
