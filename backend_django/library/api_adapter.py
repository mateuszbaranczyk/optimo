import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional

import requests
from library.serializers import ReserveSerializer
from rest_framework.serializers import ModelSerializer

logger = logging.getLogger("api_errors")


class RequestException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        logger.info(f"API error: {args}")


@dataclass(frozen=True)
class BookStatus:
    title: str
    available: int
    total: int


@dataclass(frozen=True)
class ReservationStatus:
    reservation: str


class Requester(ABC):
    domain: str

    @abstractmethod
    def send_validated(
        self, serializer: ModelSerializer, url: str
    ) -> requests.Response:
        raise NotImplementedError

    def handle_errors(self, response: requests.Response) -> Optional[None]:
        status = response.status_code
        url = response.url
        match status:
            case HTTPStatus.OK | HTTPStatus.CREATED:
                return None
            case HTTPStatus.BAD_REQUEST:
                raise RequestException("BAD_REQUEST " + url)
            case HTTPStatus.NOT_FOUND:
                raise RequestException("NOT_FOUND " + url)
            case HTTPStatus.INTERNAL_SERVER_ERROR:
                raise RequestException("INTERNAL_SERVER_ERROR " + url)
            case _:
                raise RequestException(f"{url}Status code: {status},")


class FlaskApi(Requester):
    host = os.getenv("FLASK_HOST", "flaskhost")
    port = os.getenv("FLASK_PORT", "5013")
    domain = f"http://{host}:{port}/"
    TIMEOUT = 1

    def status(self, book_id: int) -> BookStatus:
        status_endpoint = f"status/{book_id}/"
        url = self.domain + status_endpoint
        response = requests.get(url, timeout=self.TIMEOUT)
        self.handle_errors(response)
        json = response.json()
        return BookStatus(**json)

    def reserve(self, reservation: ReserveSerializer) -> ReservationStatus:
        reserve_endpoint = "reserve/"
        url = self.domain + reserve_endpoint
        response = self.send_validated(reservation, url)
        self.handle_errors(response)
        json = response.json()
        return ReservationStatus(**json)

    def send_validated(
        self, reservation: ReserveSerializer, url: str
    ) -> requests.Response:
        if reservation.is_valid(raise_exception=True):
            data = reservation.validated_data
            response = requests.post(url, json=data, timeout=self.TIMEOUT)
            return response

    def handle_errors(self, response: requests.Response) -> None:
        return super().handle_errors(response)
