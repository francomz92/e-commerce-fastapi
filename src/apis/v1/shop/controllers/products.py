from uuid import UUID
from fastapi import status
from fastapi.exceptions import HTTPException

from .....utils.constants import ERROR__UPLOAD_FILE, ERROR__NOT_FOUND
from .....helpers.files import FileHandler
from .....handlers.errors import NotFoundError
from .....schemas import ProductCreationSchema, ProductModificationSchema
from .....models import Product, Category
from .....services.transactions import ProductTransaction, CategoryTransaction
from ....dependencies.connections import Session
from ..services.filters import ProductFilter
from ..schemas import ProductStoreCreationSchema, ProductStoreModificationSchema
from ..schemas.filters import ProductQueryParams


class ProductsController:
    def __init__(self, session: Session) -> None:
        self._db = session

    async def create_product(self, raw_data: ProductStoreCreationSchema):
        uploaded_path = FileHandler.upload_image(
            raw_data.media, path=f'products/{raw_data.media.filename}'
        )
        if not uploaded_path:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ERROR__UPLOAD_FILE
            )
        creation_schema = ProductCreationSchema(
            **raw_data.model_dump(exclude={'media', 'image'}), image=uploaded_path
        )
        return await ProductTransaction(self._db).create(creation_schema)

    async def get_product(self, _id: UUID):
        return await ProductTransaction(self._db).get_by_id(_id)

    async def list_products(self, query_params: ProductQueryParams):
        products = await ProductTransaction(self._db).where(
            skip=query_params.skip,
            limit=query_params.limit,
            order_by='name',
            **query_params.model_dump(
                exclude={'skip', 'limit', 'order_by', 'categories'}, exclude_none=True
            ),
        )
        if query_params.categories:
            products = ProductFilter.filter_by_categories(products, query_params.categories)
        return products

    async def update_product(self, _id: UUID, raw_data: ProductStoreModificationSchema):
        product = await ProductTransaction(self._db).get_by_id(_id)
        if not product:
            raise NotFoundError(msg=ERROR__NOT_FOUND % 'producto')

        if raw_data.media and raw_data.media.size:
            error_during_upload = HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ERROR__UPLOAD_FILE
            )

            is_deleted = FileHandler.delete_image(product.image)
            if not is_deleted:
                raise error_during_upload

            uploaded_path = FileHandler.upload_image(
                raw_data.media, path=f'products/{raw_data.media.filename}'
            )
            if not uploaded_path:
                raise error_during_upload

            raw_data.image = uploaded_path
        modification_schema = ProductModificationSchema(
            **raw_data.model_dump(
                exclude={'media'}, exclude_none=True, exclude_unset=True
            )
        )
        updated_product = await ProductTransaction(self._db).update(
            product, modification_schema
        )

        # current_product_categories_ids = [category.id for category in product.categories]
        # for category_id in raw_data.categories:
        #     if category_id in current_product_categories_ids:
        #         continue
        #     category = await CategoryTransaction(self._db, Category).get_by_id(category_id)
        #     updated_product.categories.append(category)
        return updated_product

    async def delete_product(self, _id: UUID):
        product = await ProductTransaction(self._db).get_by_id(_id)
        if not product:
            raise NotFoundError(msg=ERROR__NOT_FOUND % 'producto')
        return await ProductTransaction(self._db).delete(product)
