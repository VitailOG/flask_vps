import requests

from http import HTTPStatus
from typing import Any, ClassVar, Literal


class HTTPStatusError(Exception):
    pass


class BaseFetcher:
    url: str
    context: ClassVar[dict[str, Any]]
    method: ClassVar[Literal['get', 'post', 'patch', 'put']]

    def fetch(self):
        response = getattr(requests, self.method)(self.url, **self.context)

        if response.status_code != HTTPStatus.OK:
            raise HTTPStatusError

        return response

    def json(self):
        return self.fetch().json()

    def iter_content(self, chunk: int):
        return self.fetch().iter_content(chunk)


class UserCoordinateFetcher(BaseFetcher):
    method = "get"
    url = "http://api.ipapi.com/api/"
    context = {
        "params": {
            "access_key": "65df7c82ddb887fad4c61c3fb1459039"
        }
    }

    def __init__(self, ip: str):
        self.url = f"{self.url}{ip}"


class ContentFetcher(BaseFetcher):
    method = "get"
    url = ""
    context = {"stream": True}

    def __init__(self, file_url: str):
        self.url = f"{self.url}{file_url}"
