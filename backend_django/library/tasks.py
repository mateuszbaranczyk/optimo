from datetime import datetime

from celery import shared_task
from library.models import Reservation


@shared_task
def send_emails():
    today = datetime.now()
    reservations = Reservation.objects.filter(due_date=today).iterator()
    for reservation in reservations:
        send_reservation_expired(
            reservation.user.email,
            reservation.book.title,
            reservation.due_date,
        )


def send_reservation_expired(email: str, book_title: str, due_date: datetime):
    print(f"Sending to: {email}. -> Reservation for{book_title} expired at {due_date}")
