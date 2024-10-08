# Generated by Django 5.1 on 2024-08-16 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0003_alter_book_table_alter_reservation_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("time", models.DateTimeField(auto_now_add=True)),
                ("level", models.CharField(max_length=6)),
                ("msg", models.TextField()),
            ],
            options={
                "db_table": "logs",
            },
        ),
    ]
