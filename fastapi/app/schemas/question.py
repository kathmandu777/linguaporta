from pydantic import BaseModel, Field

from ..models import Question
from .unit import ReadUnitSchema


class ReadQuestionSchema(BaseModel):
    unit: ReadUnitSchema
    number: int
    text: str
    answer: str

    class Config:
        orm_mode = True


class CreateQuestionSchema(BaseModel):
    number: int = Field(..., gt=0)
    text: str = Field(..., max_length=Question.MAX_LENGTH_TEXT)
    answer: str = Field(..., max_length=Question.MAX_LENGTH_ANSWER)

    class Config:
        orm_mode = True
