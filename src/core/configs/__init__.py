from functools import lru_cache

from .base import Settings



@lru_cache
def _get_settings():
    return Settings() # type: ignore

settings = _get_settings()