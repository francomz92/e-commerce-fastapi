from fastapi import APIRouter

from .views import products, files

router = APIRouter(prefix='/store')

router.include_router(products.router)
router.include_router(files.router)