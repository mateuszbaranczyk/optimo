from logging import Handler

from django.apps import apps


class DbHandler(Handler):
    def emit(self, record) -> None:
        LogEntry = apps.get_model("library", "LogEntry")
        entry = LogEntry(level=record.levelname, msg=record.getMessage())
        entry.save()
