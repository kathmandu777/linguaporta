from pydantic import BaseModel, Field

from ..models import Unit


class ReadUnitSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CreateUnitSchema(BaseModel):
    name: str = Field(..., max_length=Unit.MAX_LENGTH_NAME)
