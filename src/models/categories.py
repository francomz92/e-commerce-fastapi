from typing import List
from sqlalchemy.orm import relationship

from ..utils.formaters import StrignFormater
from ..db.models import BaseModel, Mapped, mapped_column, String, Boolean, Integer


class Category(BaseModel):
    __tablename__: str = 'category'

    name: Mapped[str] = mapped_column(String(length=64), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(length=64), nullable=False, default=StrignFormater.to_slug
    )
    products: Mapped[List['Product']] = relationship(secondary='product_category', back_populates='categories')  # type: ignore
    in_offer: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    discount: Mapped[int] = mapped_column(Integer, nullable=True, default=0)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Category(name={self.name}, slug={self.slug})'
