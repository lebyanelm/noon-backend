# dependencies
import json
import models.http_codes as http_codes
from flask import make_response
from models.time_created import TimeCreated


class Response():
    def __init__(self, code: int, reason=None, data=None, message=None):
        try:
            # parse the code to a proper type
            self.status_code = str(code)
            self.time_created = TimeCreated().__dict__

            if message != None:
                self.status_message = message
            else:
                # propely format the response message
                self.status_message = http_codes.HTTP_CODES[code][0]

            if reason == None:
                self.reason = http_codes.HTTP_CODES[code][1]
            else:
                if reason != None:
                    self.reason = reason

            if data != None:
                self.data = data

        except KeyError as error:
            print('Invalid status code')

    def to_json(self):
        response = make_response(json.dumps(
            self.__dict__), int(self.status_code))
        response.headers['Content-Type'] = 'application/json'
        return response
