from fastapi import APIRouter

from .health import health_router
from .unit_question import unit_router

api_router = APIRouter()
api_router.include_router(unit_router, prefix="/units", tags=["units"])
