import uvicorn

from src.core.configs import settings


if __name__ == '__main__':
    uvicorn.run(
        'src.main:get_app',
        host=settings.HOST,
        port=settings.PORT,
        factory=True,
        reload=settings.DEBUG
    )