from logging import getLogger

from app.models import Question
from app.schemas import CreateQuestionSchema
from asgiref.sync import sync_to_async

from fastapi import Request

logger = getLogger(__name__)


class QuestionAPI:
    @classmethod
    async def gets(
        cls,
        request: Request,
        unit_id: int,
    ) -> list[Question]:
        return await sync_to_async(list)(Question.objects.filter(unit=unit_id))

    @classmethod
    async def get(
        cls,
        request: Request,
        unit_id: int,
        number: int,
    ) -> Question:
        return await Question.objects.aget(unit=unit_id, number=number)

    @classmethod
    async def create(
        cls,
        request: Request,
        unit_id: int,
        schema: CreateQuestionSchema,
    ) -> Question:
        return await sync_to_async(Question.objects.create)(
            unit_id=unit_id, **schema.dict()
        )
