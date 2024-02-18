from enum import Enum


class ResponseType(Enum):
    ANSWER = "ANSWER"
    CODE = "CODE"


class Response:
    def __init__(self, responseType: ResponseType, text: str):
        self.responseType = responseType
        self.text = text
