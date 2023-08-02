import tempfile

from typing import Any
from datetime import datetime

from helpers import timeit
from fetcher import ContentFetcher
from interfaces import ClientInterface
from config import ADDRESS_BACKEND, CHUNK_SIZE


class Storage:

    def __init__(self, client: ClientInterface):
        self.client = client

    @staticmethod
    def _fetch_file(url: str, temp_file):
        for chunk in ContentFetcher(url).iter_content(chunk=CHUNK_SIZE):
            temp_file.write(chunk)
        temp_file.seek(0)
        return temp_file

    @staticmethod
    def _prepare_response(duration, server_name, city, ip, filename):
        response = {
            "duration": duration,
            "vps": server_name,
            "city": city,
            "ip": ip,
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }

        if filename is not None:
            response['link'] = f"http://{ADDRESS_BACKEND}/download/{filename}"

        return response

    def __call__(self, method, method_kwargs, **kwargs) -> tuple[Any, dict]:
        res, duration = getattr(self, method)(**method_kwargs)
        return res, self._prepare_response(**kwargs | {"filename": method_kwargs['filename'], "duration": duration})

    @timeit
    def upload(self, filename: str, url: str):
        with tempfile.NamedTemporaryFile() as temp_file:
            return self.client.upload(filename, self._fetch_file(url, temp_file))

    @timeit
    def get(self, filename: str):
        temp_file = tempfile.NamedTemporaryFile()
        return self.client.get(filename, temp_file)
