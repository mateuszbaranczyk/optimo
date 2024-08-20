from dataclasses import dataclass
from datetime import datetime

import sqlalchemy as sa
from db import db


@dataclass
class ReservationRequest:
    user_id: int
    book_id: int
    reserved_at: str
    due_date: str

    def __post_init__(self) -> None:
        self._validate()
        self._convert_date()

    def _validate(self) -> None:
        if not isinstance(self.user_id, int) or not isinstance(self.book_id, int):
            raise TypeError
        if not isinstance(self.reserved_at, str) or not isinstance(
            self.reserved_at, str
        ):
            raise TypeError
        return None

    def _convert_date(self) -> None:
        self.reservation_date = datetime.fromisoformat(self.reserved_at)
        self.expire_at = datetime.fromisoformat(self.due_date)
        return None


class Reservation(db.Model):
    __tablename__ = "reservations"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer)
    book_id = sa.Column(sa.Integer)
    reserved_at = sa.Column(sa.DateTime)
    due_date = sa.Column(sa.DateTime)


class Book(db.Model):
    __tablename__ = "books"
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(length=255))
    author = sa.Column(sa.String(length=255))
    total_copies = sa.Column(sa.Integer)
    available_copies = sa.Column(sa.Integer)
