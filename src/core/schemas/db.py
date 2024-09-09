from pydantic import BaseModel


class DBConfig(BaseModel):
    HOST: str = 'localhost'
    PORT: int = 5432
    NAME: str = 'ecommerce'
    USER: str = 'postgres'
    PASSWORD: str = 'root'

    @property
    def URI(self) -> str:
        return (
            'postgresql+asyncpg://'
            + f'{self.USER}:{self.PASSWORD}@'
            + f'{self.HOST}:{self.PORT}/'
            + f'{self.NAME}'
        )