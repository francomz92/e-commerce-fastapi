from typing import List
from decimal import Decimal
from sqlalchemy.orm import relationship

from ..utils.formaters import StrignFormater
from ..db.models import (
    Base,
    BaseModel,
    Mapped,
    mapped_column,
    Uuid,
    uuid4,
    String,
    Text,
    Double,
    Integer,
    Boolean,
    ForeignKey,
)


class ProductCategory(Base):
    """Tabla que maneja la relación ManyToMany entre productos y categorías"""

    __tablename__ = 'product_category'

    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True, default=uuid4, index=True)
    product_id: Mapped[Uuid] = mapped_column(
        Uuid, ForeignKey('product.id', ondelete='CASCADE'), primary_key=True
    )
    category_id: Mapped[Uuid] = mapped_column(
        Uuid, ForeignKey('category.id', ondelete='CASCADE'), primary_key=True
    )


class Product(BaseModel):
    __tablename__: str = 'product'

    name: Mapped[str] = mapped_column(String(length=64), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(length=64), nullable=False, default=StrignFormater.to_slug
    )
    barcode: Mapped[str] = mapped_column(String(length=12), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Double(decimal_return_scale=2), nullable=False)
    image: Mapped[str] = mapped_column(String(length=128), nullable=False)
    in_offer: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    discount: Mapped[int] = mapped_column(Integer, nullable=True, default=0)

    categories: Mapped[List['Category']] = relationship(secondary='product_category', back_populates='products')  # type: ignore

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Product(name={self.name}, slug={self.slug}, barcode={self.barcode}, description={self.description}, price={self.price}, image={self.image})'