from uuid import uuid4
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Uuid
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.sql.sqltypes import *


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True, default=uuid4, index=True)


class BaseModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    

class CreatedByMixin(object):
    
    def __init_subclass__(cls) -> None:
        if not hasattr(cls, 'created_by'):
            raise NotImplementedError('"created_by" relationship is not implemented.')

    @declared_attr
    def created_by_id(cls) -> Mapped[int]:
        """ Generate created_by_id column automatically """
        return mapped_column(Integer, ForeignKey('user.id', ondelete='SET NULL'), nullable=True)