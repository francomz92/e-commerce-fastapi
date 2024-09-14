from fastapi import APIRouter

from .store import routers as api_v1

routers = APIRouter(prefix='/v1')

routers.include_router(api_v1.router)