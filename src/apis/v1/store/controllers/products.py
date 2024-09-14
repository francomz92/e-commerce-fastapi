from uuid import UUID
from datetime import date
from fastapi import status
from fastapi.exceptions import HTTPException

from .....constants.validation import PRODUCTS_IMAGE_EXTENSIONS
from .....constants.error_messages import INVALID_FILE_FORMAT
from .....utils.constants import ERROR__UPLOAD_FILE, ERROR__NOT_FOUND
from .....helpers.files import FileHandler
from .....handlers.errors import NotFoundError, ValidationError
from .....schemas import ProductCreationSchema, ProductModificationSchema
from .....services.transactions import ProductTransaction, CategoryTransaction
from ....dependencies.connections import Session
from ..schemas import ProductStoreCreationSchema, ProductStoreModificationSchema
from ..schemas.filters import ProductQueryParams


class ProductsController:
    def __init__(self, session: Session) -> None:
        self._db = session

    async def create_product(self, raw_data: ProductStoreCreationSchema):
        if not raw_data.media.filename:
            raise HTTPException(
                detail=ERROR__UPLOAD_FILE,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        today = date.today()
        uploaded_path = FileHandler.upload_image(
            raw_data.media,
            path=raw_data.media.filename,
            folder=f'images/products/{today.year}/{today.month}'
        )
        if not uploaded_path:
            raise HTTPException(
                detail=ERROR__UPLOAD_FILE,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
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
                exclude={'skip', 'limit', 'order_by'},
                exclude_none=True
            )
        )
        return products

    async def update_product(self, _id: UUID, raw_data: ProductStoreModificationSchema):
        product = await ProductTransaction(self._db).get_by_id(_id)
        if not product:
            raise NotFoundError(msg=ERROR__NOT_FOUND % 'producto')

        if raw_data.media and raw_data.media.size and raw_data.media.filename:
            """ Valida y Carga la imagen del producto """
            error_during_upload = HTTPException(
                detail=ERROR__UPLOAD_FILE,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
            if not FileHandler.validate_file_extension(raw_data.media, PRODUCTS_IMAGE_EXTENSIONS):
                raise ValidationError(
                    field='media',
                    msg=INVALID_FILE_FORMAT.format(', '.join(PRODUCTS_IMAGE_EXTENSIONS))
                )

            is_deleted = FileHandler.delete_image(product.image)
            if not is_deleted:
                raise error_during_upload

            today = date.today()
            uploaded_path = FileHandler.upload_image(
                media=raw_data.media,
                path=raw_data.media.filename,
                folder=f'images/products/{today.year}/{today.month}'
            )
            if not uploaded_path:
                raise error_during_upload

            raw_data.image = uploaded_path
        
        """ Actualiza los datos del producto """
        modification_schema = ProductModificationSchema(
            **raw_data.model_dump(
                exclude={'media'},
                exclude_none=True,
                exclude_unset=True
            )
        )
        updated_product = await ProductTransaction(self._db).update(
            product,
            modification_schema
        )

        """ Actualiza las categorías del producto """
        if not raw_data.categories:
            product.categories.clear()
        else:
            new_categories = raw_data.categories
            all_categories = await CategoryTransaction(self._db).all()
            valid_categories = filter(lambda x: x.id in new_categories, all_categories)
            categories_to_remove = set(product.categories) - set(valid_categories)
            categories_to_add = set(valid_categories) - set(product.categories)
            for category in categories_to_add:
                product.categories.append(category)
            for category in categories_to_remove:
                product.categories.remove(category)
        return updated_product

    async def delete_product(self, _id: UUID):
        product = await ProductTransaction(self._db).get_by_id(_id)
        if not product:
            raise NotFoundError(msg=ERROR__NOT_FOUND % 'producto')
        return await ProductTransaction(self._db).delete(product)
