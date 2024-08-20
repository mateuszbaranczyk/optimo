from library.api_adapter import FlaskApi, ReservationStatus
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from .models import Book, Reservation
from .serializers import (BookSerializer, ReservationSerialazer,
                          ReserveSerializer)


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        prev_visited = self._add_unique_to_session(request, serializer)
        serializer.context["prev_visited"] = prev_visited
        response_data = serializer.data
        return Response(response_data)

    def _add_unique_to_session(self, request, serializer):
        prev_visited = request.session.get("prev_visited", [])
        book_id = serializer.instance.id
        if book_id not in prev_visited:
            prev_visited.append(book_id)
        request.session["prev_visited"] = prev_visited
        return prev_visited


class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerialazer

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed(
            method="POST",
            detail="Please use `/reserve/`",
        )


class ReserveView(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ReserveSerializer
    api = FlaskApi()

    def post(self, request: Request) -> Response:
        reservation = ReserveSerializer(data=request.data)
        reservation.is_valid()
        book_id = reservation.validated_data["book_id"]
        if self._is_available(book_id):
            self._send_reserve_request(reservation)
        else:
            return Response({"msg": "Book not available"}, status=418)
        self._update_book_available_copies(book_id)
        return Response(reservation.validated_data, status=HTTP_201_CREATED)

    def _update_book_available_copies(self, book_id: int) -> None:
        book = Book.objects.get(id=book_id)
        book.available_copies = book.available_copies - 1
        book.save()

    def _send_reserve_request(
        self,
        reservation: ReserveSerializer,
    ) -> ReservationStatus:
        response = self.api.reserve(reservation)
        return response.reservation

    def _is_available(self, book_id: int) -> bool:
        availability = self.api.status(book_id).available
        if availability > 0:
            return True
        return False
