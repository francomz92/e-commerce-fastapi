from functools import wraps
from typing import Callable
from psycopg2.errors import UniqueViolation
from asyncpg.exceptions import UniqueViolationError

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from ..handlers.errors import ValidationError


def transaction(func):
    """ Decorator to controling errors in data base transactions. """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as err:
            if hasattr(err, 'orig') and err.orig.__class__ == UniqueViolationError: # type: ignore
                orig: UniqueViolationError = err.orig # type: ignore
                field = orig.diag.constraint_name.split('_')[1:-1][0] # type: ignore
                raise ValidationError(field=field, msg='Ya existe')
            raise HTTPException(500, 'Internal server error')
        return result
    return wrapper

def atomic(func: Callable):
    """ Decorator to controling rollback changes in data base transactions """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        db: AsyncSession = kwargs.get('db', None)
        if db is None:
            raise KeyError(f'kwargs of {func.__name__} does not have the attribute.')
        try:
            result = await func(*args, **kwargs)
            await db.commit()
        except Exception as err:
            await db.rollback()
            raise err
        finally:
            await db.close()
        return result
    return wrapper