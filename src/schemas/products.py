from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ValidationInfo
from pydantic.functional_validators import field_validator

from ..schemas.categories import CategorySchema


class BaseProductSchema(BaseModel):
    name: str
    slug: str
    description: str
    barcode: str
    price: float


class ProductSchema(BaseProductSchema):
    id: Optional[UUID] = None
    image: Optional[str] = None
    in_offer: Optional[bool] = False
    discount: Optional[int] = 0
    price_with_discount: Optional[float] = 0
    categories: List[CategorySchema] = []

    class Config:
        from_attributes = True

    @field_validator('price_with_discount')
    def validate_price_with_discount(cls, v: float, info: ValidationInfo):
        if info.data.get('in_offer'):
            _discount = 0
            for category in info.data.get('categories', []):
                if category.in_offer:
                    _discount = category.discount
            _discount += info.data.get('discount', 0)
            return info.data.get('price', 0) * _discount / 100
        return info.data.get('price')


class ProductCreationSchema(BaseProductSchema):
    description: Optional[str]
    image: Optional[str] = None
    in_offer: Optional[bool] = False
    discount: Optional[int] = 0
    categories: List[CategorySchema] = []



class ProductModificationSchema(BaseModel):
    name: Optional[str]
    slug: Optional[str]
    description: Optional[str]
    barcode: Optional[str]
    price: Optional[float]
    image: Optional[str]
    in_offer: Optional[bool]
    discount: Optional[int]
    categories: Optional[List[UUID]] = []