import os

from .base import *  # noqa

DEBUG = False

# set string like "localhost,example.com"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
