from typing import Annotated, List
from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from .....db.decorators import atomic
from .....schemas import ProductSchema
from ....dependencies.connections import get_db, Session
from ..schemas import ProductStoreCreationSchema, ProductStoreModificationSchema
from ..schemas.filters import ProductQueryParams
from ..controllers import ProductsController


router = APIRouter(prefix='/products', tags=['Productos'])


@router.post(
    '',
    response_model=ProductSchema,
    description='Almacena un nuevo producto en la base de datos',
    summary='Crear un nuevo producto',
)
@atomic
async def create_product(
    db: Annotated[Session, Depends(get_db)],
    data: ProductStoreCreationSchema = Depends(ProductStoreCreationSchema.as_form),
):
    product = await ProductsController(db).create_product(data)
    return ProductSchema.model_validate(product)


@router.get(
    '/{product_id}',
    response_model=ProductSchema,
    description='Obtiene un producto por su id de la base de datos',
    summary='Retornar un producto',
)
async def get_product(db: Annotated[Session, Depends(get_db)], product_id: UUID):
    return await ProductsController(db).get_product(product_id)


@router.get(
    '',
    response_model=List[ProductSchema],
    description='Lista todos los productos de la base de datos',
    summary='Listar productos',
)
async def list_products(
    db: Annotated[Session, Depends(get_db)],
    query_params: Annotated[ProductQueryParams, Depends(ProductQueryParams.parser)],
):
    return await ProductsController(db).list_products(query_params)


@router.put(
    '/{product_id}',
    response_model=ProductSchema,
    description='Actualizar un producto de la base de datos',
    summary='Actualizar un producto',
)
@atomic
async def update_product(
    db: Annotated[Session, Depends(get_db)],
    product_id: UUID,
    data: Annotated[
        ProductStoreModificationSchema, Depends(ProductStoreModificationSchema.as_form)
    ],
):
    product = await ProductsController(db).update_product(product_id, data)
    # return ProductSchema.model_validate(product)
    return product


@router.delete(
    '/{product_id}',
    response_class=JSONResponse,
    description='Elimina un producto de la base de datos',
    summary='Eliminar un producto',
)
@atomic
async def delete_product(db: Annotated[Session, Depends(get_db)], product_id: UUID):
    await ProductsController(db).delete_product(product_id)
    return JSONResponse(content={'detail': 'Producto eliminado correctamente.'})
