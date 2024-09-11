from typing import Type
from pydantic import UUID4
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from ...helpers.transactions import Transaction, transaction
from ...models import Category
from ...schemas import CategoryCreationSchema, CategoryModificationSchema


class CategoryTransaction(Transaction[Category, CategoryCreationSchema, CategoryModificationSchema]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Category)

    @transaction
    async def get_by_id(self, _id: UUID4):
        statment = super().get_by_id(_id) # .options(selectinload(self.model.products))
        result = await self.db.execute(statment)
        return result.scalar_one_or_none()
    
    @transaction
    async def where(self, skip: int, limit: int, order_by: str, **kwargs):
        statment = super().where(skip, limit, order_by, **kwargs) # .options(selectinload(self.model.products))
        result = await self.db.execute(statment)
        return result.scalars()._allrows()
    
    @transaction
    async def all(self):
        statment = super().all()
        result = await self.db.execute(statment)
        return result.scalars()._allrows()