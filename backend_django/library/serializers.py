from datetime import datetime

from rest_framework import serializers

from .models import Book, Reservation


class BookSerializer(serializers.ModelSerializer):
    prev_visited = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "__all__"

    def get_prev_visited(self, obj):
        prev_visited = self.context.get("prev_visited", [])
        if prev_visited:
            books = Book.objects.filter(id__in=prev_visited)
            return BookSerializer(books, many=True).data
        else:
            return []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        prev_visited_length = len(representation.get("prev_visited", []))
        if prev_visited_length == 0:
            representation.pop("prev_visited", None)
        return representation


class ReserveSerializer(serializers.ModelSerializer):
    def validate(self, data: dict):
        data["reserved_at"] = datetime.now().isoformat()
        data["due_date"] = data["due_date"].isoformat() if data["due_date"] else None
        data["user_id"] = data.pop("user")
        data["user_id"] = data["user_id"].id
        data["book_id"] = data.pop("book")
        data["book_id"] = data["book_id"].id
        return data

    class Meta:
        model = Reservation
        fields = "__all__"


class ReservationSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
