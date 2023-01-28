from app.models import User
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Receive, Scope, Send


# should be set after AuthorizerMiddleware
class ApiKeyUsedTimesCountMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope)

        api_key = conn.headers.get("x-api-key", "")
        user = await User.objects.filter(api_key=api_key).afirst()
        if user:
            user.api_key_used_times += 1
            user.save()
        return await self.app(scope, receive, send)
