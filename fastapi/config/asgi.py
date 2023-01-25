"""ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

"""
Settings
"""
env_state = os.getenv("ENV_STATE", "production")
if env_state == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
elif env_state == "staging":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.staging")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")


"""
Django settings
"""
django_app = get_asgi_application()


"""
FastAPI settings
"""
from app.routers import api_router, health_router
from django.conf import settings
from fastapi_key_auth import AuthorizerMiddleware

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

fastapi_app = FastAPI(
    title="LinguaPorta Answer API",
    description="This is a REST API for LinguaPorta Answer",
    version="0.1.0",
)


# CORS
if not settings.DEBUG:
    fastapi_app.add_middleware(
        AuthorizerMiddleware,
        public_paths=["^/docs*", "/openapi.json", "^/redoc*", "^/django*"],
        key_pattern="API_KEY_",
    )
    fastapi_app.add_middleware(
        CORSMiddleware,
        # set string like "http://localhost:8000,https://example.com"
        allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# routers
fastapi_app.include_router(health_router, tags=["health"], prefix="/health")
fastapi_app.include_router(api_router, prefix="/api")

# django (when local run)
if settings.DEBUG:
    fastapi_app.mount("/django", django_app)
    fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")
