from typing import Any, Dict
from starlette.config import EnvironError
from pydantic_settings import BaseSettings as BaseConfig, SettingsConfigDict
from pydantic import field_validator

from ..schemas.db import DBConfig
from ..schemas.cors import CorsConfig


class Settings(BaseConfig):
    ENVIRONMENT: str
    SECRET_KEY: str = 'secret'
    TIME_ZONE: str
    BASE_URL_BACKEND: str = 'http://localhost:8000'
    HOST: str = '0.0.0.0'
    PORT: int = 8000

    DB: DBConfig = DBConfig() # type: ignore
    CORS: CorsConfig = CorsConfig() # type: ignore

    DOCKS_URL: str = '/docs'
    OPENAPI_PREFIX: str = ''
    OPENAPI_URL: str = '/openapi.json'
    REDOC_URL: str = '/redoc'
    TITLE: str = 'Basic e-commerce API'
    VERSION: str = '1.0'

    model_config = SettingsConfigDict(env_file=('.env', '.env.prod'), env_nested_delimiter='__', extra='ignore')

    @property
    def DEBUG(self) -> bool:
        return self.ENVIRONMENT == 'dev'
    
    @property
    def DISABLE_DOCS(self):
        return not self.DEBUG
    
    @property
    def ADMIN_USER(self):
        return 'admin' if self.DEBUG else None
    
    @property
    def ADMIN_PASSWORD(self):
        return 'admin' if self.DEBUG else None


    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        kwargs = {
            'debug': self.DEBUG,
            'docs_url': self.DOCKS_URL,
            'openapi_prefix': self.OPENAPI_PREFIX,
            'openapi_url': self.OPENAPI_URL,
            'redoc_url': self.REDOC_URL,
            'title': self.TITLE,
            'version': self.VERSION,
        }
        if self.DISABLE_DOCS:
            kwargs.update({
                'docs_url': self.DOCKS_URL,
                'openapi_url': self.OPENAPI_URL,
                'redoc_url': self.REDOC_URL,
            })
        return kwargs
    
    @field_validator('ENVIRONMENT')
    def check_enviroment(cls, value: str):
        if value not in ('dev', 'prod'):
            raise EnvironError(f'Invalid enviroment: {value}')
        return value