from typing import Protocol


class ClientInterface(Protocol):

    def get(self, filename: str, buffer) -> None:
        ...

    def upload(self, filename: str, data) -> None:
        ...
