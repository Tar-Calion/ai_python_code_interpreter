from enum import Enum


class ResponseType(Enum):
    ANSWER = "ANSWER"
    CODE = "CODE"


class Response:
    def __init__(self, type: ResponseType, text: str):
        self.type = type
        self.text = text
