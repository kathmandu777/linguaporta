from app.api import QuestionAPI, UnitAPI
from app.models import Question, Unit
from app.schemas import (
    CreateQuestionSchema,
    CreateUnitSchema,
    ReadQuestionSchema,
    ReadUnitSchema,
)

from fastapi import APIRouter, Request

unit_router = APIRouter()


@unit_router.get(
    "/",
    response_model=list[ReadUnitSchema],
    status_code=200,
)
async def get_units(
    request: Request,
) -> list[Unit]:
    return await UnitAPI.gets(request)


@unit_router.post(
    "/",
    response_model=ReadUnitSchema,
    status_code=201,
)
async def create_unit(
    request: Request,
    schema: CreateUnitSchema,
) -> Unit:
    return await UnitAPI.create(request, schema)


@unit_router.get(
    "/{unit_id}/questions",
    response_model=list[ReadQuestionSchema],
    status_code=200,
)
async def get_questions(
    request: Request,
    unit_id: int,
) -> list[Question]:
    return await QuestionAPI.gets(request, unit_id)


@unit_router.post(
    "/{unit_id}/questions",
    response_model=ReadQuestionSchema,
    status_code=201,
)
async def create_question(
    request: Request,
    unit_id: int,
    schema: CreateQuestionSchema,
) -> Question:
    return await QuestionAPI.create(request, unit_id, schema)
