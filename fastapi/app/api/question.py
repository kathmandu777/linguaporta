from logging import getLogger

from app.models import Question, User
from app.schemas import CreateQuestionSchema
from asgiref.sync import sync_to_async

from fastapi import HTTPException, Request

logger = getLogger(__name__)


class QuestionAPI:
    @classmethod
    async def gets(
        cls,
        request: Request,
        unit_id: int,
    ) -> list[Question]:
        api_key = request.headers.get("X-API-KEY")
        if not api_key:
            raise HTTPException(401, "X-API-KEY is not found.")

        user = await User.objects.filter(api_key=api_key).afirst()
        if not user or not user.is_active:
            raise HTTPException(401, "Invalid API key.")

        if not user.can_get_questions:
            raise HTTPException(403, "API key usage limit has been reached. Please reissue.")
        user.get_questions_count += 1
        user.save()
        return await sync_to_async(list)(Question.objects.filter(unit=unit_id))

    @classmethod
    async def create(
        cls,
        request: Request,
        unit_id: int,
        schema: CreateQuestionSchema,
    ) -> Question:
        obj, _ = await sync_to_async(Question.objects.update_or_create)(
            unit_id=unit_id, number=schema.number, defaults=schema.dict()
        )
        return obj
