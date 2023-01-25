from django.db import models

from .base import TimestampModelMixin
from .question import Question


class Unit(TimestampModelMixin):
    MAX_LENGTH_NAME = 32
    name = models.CharField(max_length=MAX_LENGTH_NAME, unique=True)

    def __str__(self) -> str:
        return f"Unit - {self.name}"

    @property
    def questions(self) -> list["Question"]:
        return list(self.question_set.all())
