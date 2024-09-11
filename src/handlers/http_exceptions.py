import sys
from typing import Union

from fastapi import status, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.exception_handlers import http_exception_handler as _http_exception_handler
from fastapi.responses import Response, JSONResponse, PlainTextResponse

from ..utils.logger import logger
from ..utils.i18n import Translate


async def http_request_validation_error_exception_handler(request: Request, exc: RequestValidationError) -> Response:
    """
    This middleware is responsible for handling request validation exceptions.
    Formats the response, if an error occurs in the middleware it is recorded in the log.
    """
    response_data = {}
    _errors = Translate.translate(list(exc.errors()), locale='es')
    try:
        for error in _errors:
            if error.get('msg', None) is not None:
                msg = error['msg']
            else:
                context = error['ctx']
                msg = context['error'] if context.get('error', None) else context['reason']
            field = '.'.join(map(lambda x: str(x), error['loc'][1:]))
            response_data[field] = msg
    except Exception as err:
        method = request.method.upper()
        path = f'{request.url.path}?{request.path_params}' if request.path_params else request.url.path
        exception = exc.__class__.__name__
        _details = exc.__context__.args if exc.__context__ else exc.body
        detail = f'{method} - {path} {exception} {_details}'
        logger.error(detail)
        raise err
    return JSONResponse(content=response_data, status_code=status.HTTP_400_BAD_REQUEST)


async def http_exception_handler(request: Request, exc: HTTPException) -> Union[JSONResponse, Response]:
    """
    This is a wrapper to the default HTTPException handler of FastAPI.
    This function will be called when a HTTPException is explicitly raised.
    """
    method = request.method.upper()
    path = f'{request.url.path}?{request.path_params}' if request.path_params else request.url.path
    exception = exc.__class__.__name__
    _details = exc.__context__.args if exc.__context__ else exc.detail
    detail = f'{method} - {path} {exception} {_details}'
    logger.error(detail)
    return await _http_exception_handler(request, exc)


async def unhandled_exception_handler(request: Request, exc: Exception) -> PlainTextResponse:
    """
    This middleware will log all unhandled exceptions.
    Unhandled exceptions are all exceptions that are not HTTPExceptions or RequestValidationErrors.
    """
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    _details = getattr(exc.__context__, 'args')
    exception_type, exception_value, _ = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    logger.error(f'{request.method.upper()} {url}" 500 Internal Server Error <{exception_name}: {exception_value}>: {_details}')
    return PlainTextResponse(str(exc), status_code=500)