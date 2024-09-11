from abc import abstractmethod
from typing import Generic, Type, TypeVar
from uuid import UUID
from pydantic import BaseModel, UUID4
# from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio.session import AsyncSession as Session

from ..db.models import Base
from ..db.decorators import transaction


ModelType = TypeVar('ModelType', bound=Base)
CreationSchemaType = TypeVar('CreationSchemaType', bound=BaseModel)
ModificationSchemaType = TypeVar('ModificationSchemaType', bound=BaseModel)


class Transaction(Generic[ModelType, CreationSchemaType, ModificationSchemaType]):

    def __init__(self, session: Session, model: Type[ModelType]) -> None:
        self.__db = session
        self.__model = model
    
    @property
    def db(self) -> Session:
        return self.__db
    
    @property
    def model(self):
        return self.__model

    @transaction
    async def create(self, raw_data: CreationSchemaType):
        data = self.model(**raw_data.model_dump())
        self.db.add(data)
        await self.db.flush([data])
        return data

    def get_by_id(self, _id: UUID4):
        statment = select(self.model).where(self.model.id == _id.hex)
        return statment

    def update(self, db_data: ModelType, raw_data: dict):
        for key, value in raw_data.items():
            setattr(db_data, key, value)
        return db_data
    
    def where(self, skip: int, limit: int, order_by: str, **kwargs):
        statment = select(self.model)
        for key, value in kwargs.items():
            statment = statment.filter(getattr(self.model, key).icontains(value))
        return statment.order_by(order_by).offset(skip).limit(limit)
    
    @transaction
    async def delete(self, obj: ModelType):
        return await self.db.delete(obj)
    
    @abstractmethod
    def all(self):
        statment = select(self.model)
        return statment