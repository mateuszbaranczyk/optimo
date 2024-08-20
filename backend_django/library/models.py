from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} - available {self.available_copies}/{self.total_copies}"

    class Meta:
        db_table = "books"


class Reservation(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.user} reserved {self.book} from {self.reserved_at} to {self.due_date}"

    class Meta:
        db_table = "reservations"


class LogEntry(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=6)
    msg = models.TextField()

    class Meta:
        db_table = "logs"
