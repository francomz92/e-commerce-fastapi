from pydantic import UUID4
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from ...helpers.transactions import Transaction, transaction
from ...models import Product, Category
from ...schemas import ProductCreationSchema, ProductModificationSchema


class ProductTransaction(Transaction[Product, ProductCreationSchema, ProductModificationSchema]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Product)
    
    @transaction
    async def get_by_id(self, _id: UUID4):
        statment = super().get_by_id(_id).options(selectinload(self.model.categories))
        result = await self.db.execute(statment)
        return result.scalar_one_or_none()
    
    @transaction
    async def where(self, skip: int, limit: int, order_by: str, **kwargs):
        categories = kwargs.pop('categories', [])
        statment = super().where(skip, limit, order_by, **kwargs).options(selectinload(self.model.categories))
        if categories:
            statment = statment.join(self.model.categories).filter(
                Category.slug.in_(categories)
            )
        result = await self.db.execute(statment)
        return result.scalars().all()

    @transaction
    async def update(self, db_data: Product, raw_data: ProductModificationSchema):
        product = super().update(
            db_data,
            raw_data.model_dump(
                exclude={'categories'},
                exclude_none=True,
                exclude_unset=True
            )
        )
        await self.db.flush([product])
        return product
