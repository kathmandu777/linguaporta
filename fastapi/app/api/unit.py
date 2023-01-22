from logging import getLogger

from app.models import Unit
from app.schemas import CreateUnitSchema
from asgiref.sync import sync_to_async

from fastapi import Request

logger = getLogger(__name__)


class UnitAPI:
    @classmethod
    async def gets(
        cls,
        request: Request,
    ) -> list[Unit]:
        return await sync_to_async(list)(Unit.objects.all())

    @classmethod
    async def create(
        cls,
        request: Request,
        schema: CreateUnitSchema,
    ) -> Unit:
        return await sync_to_async(Unit.objects.create)(**schema.dict())
