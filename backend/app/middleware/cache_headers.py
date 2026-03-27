from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class CacheHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        path = request.url.path

        if path.startswith("/static/images/"):
            # Cached images — tell browser to cache for 30 days
            response.headers["Cache-Control"] = (
                "public, max-age=2592000, immutable"
            )
        elif path.startswith("/api/"):
            # API responses — no caching by default
            response.headers["Cache-Control"] = (
                "no-cache, no-store, must-revalidate"
            )

        return response