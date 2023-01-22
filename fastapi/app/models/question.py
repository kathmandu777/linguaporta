from django.db import models

from .base import TimestampModelMixin


class Question(TimestampModelMixin):
    unit = models.ForeignKey(
        "Unit",
        on_delete=models.CASCADE,
        related_name="questions",
    )

    number = models.SmallIntegerField()

    MAX_LENGTH_TEXT = 256
    text = models.CharField(max_length=MAX_LENGTH_TEXT)

    MAX_LENGTH_ANSWER = 128
    answer = models.CharField(max_length=MAX_LENGTH_ANSWER)

    class Meta:
        unique_together = ("unit", "number")
        ordering = ("unit", "number")

    def __str__(self) -> str:
        return f"Question - {self.number} [{self.unit}]"
