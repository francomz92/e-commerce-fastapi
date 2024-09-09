from typing import Dict, Optional
from fastapi import exceptions, status

class ValidationError(exceptions.RequestValidationError):

    def __init__(self, field: str = 'detail', *, msg: str) -> None:
        errors = [{
            'loc': ('', field),
            'msg': msg
        }]
        super().__init__(errors)

class NotFoundError(exceptions.HTTPException):
    def __init__(
        self,
        msg: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=msg, headers=headers)