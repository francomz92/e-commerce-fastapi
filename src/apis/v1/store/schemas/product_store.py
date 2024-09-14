from typing import Optional

from fastapi.datastructures import UploadFile
from fastapi.params import File, Form
from pydantic import field_validator

from .....handlers.errors import ValidationError
from .....schemas import ProductCreationSchema, ProductModificationSchema


class ProductStoreCreationSchema(ProductCreationSchema):
    media: UploadFile

    @field_validator('media')
    def validate_media(cls, v: UploadFile):
        if not v.size:
            raise ValidationError(field='media', msg='Debe subir una imagen.')
        return v

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),  # type: ignore
        slug: str = Form(...),  # type: ignore
        description: str = Form(...),  # type: ignore
        barcode: str = Form(...),  # type: ignore
        price: float = Form(...),  # type: ignore
        media: UploadFile = File(...),  # type: ignore
    ):
        return cls(
            name=name, slug=slug, description=description, barcode=barcode, price=price, media=media
        )


class ProductStoreModificationSchema(ProductModificationSchema):
    media: Optional[UploadFile]

    @classmethod
    def as_form(
        cls,
        name: str = Form(None),  # type: ignore
        slug: str = Form(None),  # type: ignore
        description: str = Form(None),  # type: ignore
        barcode: str = Form(None),  # type: ignore
        price: float = Form(None),  # type: ignore
        media: Optional[UploadFile] = File(None),  # type: ignore
        categories: Optional[str] = Form(None),  # type: ignore
        image: str = Form(None),  # type: ignore
        in_offer: bool = Form(None),  # type: ignore
        discount: int = Form(None),  # type: ignore
    ):
        if categories is not None:
            categories = categories.replace('"', '').split(',') # type: ignore
        return cls(
            name=name,
            slug=slug,
            description=description,
            barcode=barcode,
            price=price,
            media=media,
            categories=categories,  # type: ignore
            image=image,
            in_offer=in_offer,
            discount=discount,
        )
