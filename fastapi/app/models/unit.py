from django.db import models

from .base import TimestampModelMixin


class Unit(TimestampModelMixin):
    MAX_LENGTH_NAME = 32
    name = models.CharField(max_length=MAX_LENGTH_NAME, unique=True)

    def __str__(self) -> str:
        return f"Unit - {self.name}"
