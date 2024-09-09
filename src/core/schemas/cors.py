from typing import List
from pydantic import BaseModel


class CorsConfig(BaseModel):
    
    ALLOW_ORIGINS: List[str] = ['*']
    ALLOW_METHODS: List[str] = ['*']
    ALLOW_HEADERS: List[str] = ['*']
    ALLOW_CREDENTIALS: bool = True