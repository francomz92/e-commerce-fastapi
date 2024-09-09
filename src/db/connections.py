from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from ..core.configs import settings

engine = create_async_engine(settings.DB.URI, echo=False, future=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)