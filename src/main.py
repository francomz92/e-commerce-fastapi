from functools import lru_cache
from starlette.exceptions import HTTPException

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from .core.configs import settings
from .handlers.http_exceptions import (
    http_request_validation_error_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
)
from .apis import routers


@lru_cache
def get_app() -> FastAPI:
    """Configura el servidor para el proyecto"""

    server = FastAPI(**settings.fastapi_kwargs)
    server.mount('/static', StaticFiles(directory='static'), name='static')

    # Middlewares
    server.add_middleware(
        CORSMiddleware,
        allow_credentials=settings.CORS.ALLOW_CREDENTIALS,
        allow_origins=settings.CORS.ALLOW_ORIGINS,
        allow_methods=settings.CORS.ALLOW_METHODS,
        allow_headers=settings.CORS.ALLOW_HEADERS,
    )

    # Exception handlers
    server.add_exception_handler(
        RequestValidationError, http_request_validation_error_exception_handler
    )
    server.add_exception_handler(HTTPException, http_exception_handler)
    server.add_exception_handler(Exception, unhandled_exception_handler)

    # Routers
    server.include_router(routers.api_routers)

    @server.get('/status')
    async def status():
        return {'status': 'ok'}

    @server.get('/not-found', status_code=404)
    async def not_found():
        return {'detail': 'Not found'}

    return server
