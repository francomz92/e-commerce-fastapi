from fastapi.params import Query
from pydantic import BaseModel, Field, field_validator

from .....utils.constants import SHORT_MAX_LENGTH


class ProductQueryParams(BaseModel):
    name: str | None = Field(None, max_length=SHORT_MAX_LENGTH)
    slug: str | None = Field(None, max_length=SHORT_MAX_LENGTH)
    barcode: str | None = Field(None, max_length=SHORT_MAX_LENGTH)
    price: float | None = Field(None, max_length=SHORT_MAX_LENGTH)
    categories: list[str] = []
    skip: int
    limit: int

    @field_validator('categories')
    def validate_categories(cls, categories: list[str]):
        categories = [x for x in categories if x]
        return list(map(lambda x: x.lower(), categories))

    @classmethod
    def parser(
        cls,
        name=Query(None),
        slug=Query(None),
        barcode=Query(None),
        price=Query(None),
        categories=Query(''),
        skip=Query(0),
        limit=Query(20),
    ):
        return cls(name=name, slug=slug, barcode=barcode, price=price, categories=categories.split(','), skip=skip, limit=limit)  # type: ignore
