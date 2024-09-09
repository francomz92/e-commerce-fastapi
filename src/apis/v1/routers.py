from fastapi import APIRouter

from .shop import routers as api_v1
# from .web_sockets import routers as ws

routers = APIRouter(prefix='/v1')

routers.include_router(api_v1.router)
# routers.include_router(ws.router)