from typing import Optional
from uuid import UUID
from pydantic import BaseModel



class CategorySchema(BaseModel):
    id: Optional[UUID] = None
    name: str
    slug: str
    in_offer: Optional[bool] = False
    discount: Optional[int] = 0

    class Config:
        from_attributes = True

class CategoryModificationSchema(CategorySchema):
    pass

class CategoryCreationSchema(BaseModel):
    name: Optional[str]
    slug: Optional[str]