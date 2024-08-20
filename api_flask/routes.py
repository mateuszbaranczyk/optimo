from db import db
from flask import Blueprint, jsonify, request
from models import Book, Reservation, ReservationRequest

api = bp = Blueprint("api", __name__)


@api.route("/", methods=["GET"])
def smoke():
    return "OK"


@api.route("/status/<int:book_id>/", methods=["GET"])
def status(book_id: int):
    book = Book.query.filter_by(id=book_id).first_or_404()
    status = {
        "title": book.title,
        "total": book.total_copies,
        "available": book.available_copies,
    }
    return jsonify(status)


@api.route("/reserve/", methods=["POST"])
def reserve():
    data = request.get_json(force=True)
    try:
        validated_request = ReservationRequest(**data)
    except TypeError:
        return jsonify(msg="Request data invalid"), 400
    except ValueError:
        return jsonify(msg="Incorrect datetime format"), 400
    status = save_reservation(validated_request)
    return jsonify({"reservation": status})


def save_reservation(validated_request: ReservationRequest):
    try:
        reservation = Reservation(
            user_id=validated_request.user_id,
            book_id=validated_request.book_id,
            reserved_at=validated_request.reservation_date,
            due_date=validated_request.expire_at,
        )
        db.session.add(reservation)
        db.session.commit()
        return "ok"
    except Exception as e:
        return e
