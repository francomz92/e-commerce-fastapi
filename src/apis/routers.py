from fastapi import APIRouter

from .v1 import routers as api_v1

api_routers = APIRouter(prefix='/api')

api_routers.include_router(api_v1.routers)